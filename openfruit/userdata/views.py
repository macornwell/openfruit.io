import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.shortcuts import render, reverse
from django.utils import timezone

from openfruit.common.services import setup_user_permissions_and_groups
from openfruit.geography.models import GeoCoordinate, UserLocation
from openfruit.geography.services import GEO_DAL
from openfruit.geography.utilities import get_standardized_coordinate
from openfruit.userdata.models import UserProfile
from openfruit.userdata.forms import SignupForm


class SignupFormView(View):
    form_class = SignupForm
    initial = {'key': 'value'}
    template_name = 'userdata/signup.html'

    def __does_captcha_validate(self, captcha):
        secret = '6LdkER8UAAAAAIsCOzmyIhbEYDi0rngvu8y9pjcM',
        googleUrl = 'https://www.google.com/recaptcha/api/siteverify?secret={0}&response={1}'.format(secret, captcha)
        headers = {'content-type': 'application/json'}
        response = requests.post(googleUrl, headers=headers)
        responseData = response.json()
        return responseData['success']

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        form = self.form_class(initial=self.initial)
        data = {
            'form': form,
            'map_center': settings.DEFAULT_MAP_CENTER,
            'zipcode': '',
        }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        center = settings.DEFAULT_MAP_CENTER
        if 'new_location_lat_lon' in request.POST and request.POST['new_location_lat_lon']:
            center = request.POST['new_location_lat_lon'].split(' ', 2)
            lat = get_standardized_coordinate(center[0])
            lon = get_standardized_coordinate(center[1])
            data['new_location_lat_lon'] = '{0} {1}'.format(lat, lon)

        zipcode = data['zipcode']
        zipcodeFailed = False
        hasMoved = 'location-moved' in data and data['location-moved'] == 'moved'
        isNewLocation = data['location'] == 'new-location'

        if hasMoved:
            if zipcode:
                try:
                    data['zipcode'] = GEO_DAL.get_zipcode_by_zip(zipcode).zipcode_id
                except:
                    zipcodeFailed = True
        if not isNewLocation:
            locationID = data['existing_location']
            location = GEO_DAL.get_location_by_id(locationID)
            zipcode = location.zipcode
            if not zipcode:
                zipcode = GEO_DAL.geocode_zipcode_from_lat_lon(location.lat(), location.lon())
            data['zipcode'] = zipcode.zipcode_id

        form = self.form_class(data)
        isValid = True
        if not hasMoved and isNewLocation:
            form.add_error('__all__', 'Select a New Location.')
            isValid = False
        if zipcodeFailed:
            form.add_error('__all__', 'Zipcode could not be found.')
            isValid = False
        if form.is_valid() and isValid:
            """ TODO: REMOVE THE COMMENTS
            captcha = request.POST['g-recaptcha-response']
            captchaValidates = self.__does_captcha_validate(captcha)
            """
            captchaValidates = True
            if captchaValidates:
                signupModel = form.save(commit=False)
                valid = True
                locationError = self.__validate_location_return_error_or_location(isNewLocation, signupModel)
                if locationError:
                    form.add_error('__all__', locationError)
                    valid = False
                if valid:
                    location = None
                    if isNewLocation:
                        zipcode = signupModel.zipcode
                        latLon = signupModel.new_location_lat_lon
                        locationName = signupModel.new_location_name
                        lat, lon = latLon.split(' ')
                        coord, created = GeoCoordinate.objects.get_or_create(lat=lat, lon=lon)
                        location = GEO_DAL.create_location(zipcode, coord, locationName)
                    else:
                        location = signupModel.existing_location

                    try:
                        user = User(username=signupModel.username,
                                    first_name=signupModel.first_name,
                                    last_name=signupModel.last_name,
                                    email=signupModel.email,
                                    )
                        user.set_password(signupModel.password)
                        user.save()
                        setup_user_permissions_and_groups(user)
                        user.save()
                    except Exception as e:
                        form.add_error('__all__', e)
                        valid = False
                        try:
                            user.delete()
                        except:
                            pass

                    if valid:

                        userProfile = UserProfile(
                            organization=signupModel.organization,
                            location=location,
                            user=user
                        )
                        userProfile.save()

                        if isNewLocation:
                            userLocation = UserLocation(user=user, location=location, last_used=timezone.now(), user_created=True)
                        else:
                            userLocation = UserLocation(user=user, location=location, last_used=timezone.now(), user_created=False)
                        userLocation.save()

                        loginUrl = reverse('admin:login')
                        return HttpResponseRedirect(loginUrl)
            else:
                form.add_error('__all__', 'Captcha did not validate.')
        data = {
            'form': form,
            'map_center': center,
            'has_moved': hasMoved,
            'zipcode': zipcode,
        }
        return render(request, self.template_name, data)

    def __validate_location_return_error_or_location(self, isNewLocation, model):
        if isNewLocation:
            zipcode = model.zipcode
            latLon = model.new_location_lat_lon
            locationName = model.new_location_name
            if not zipcode:
                return 'Zipcode needed.'
            if not latLon:
                return 'Latitude and Longitude needed.'
            if not locationName:
                return 'Need name of the new location.'
        else:
            if not model.existing_location:
                return 'Need a value for an existing location.'



def signup(request):
    form = SignupForm()
    data = {
        'form': form,
        'DEFAULT_MAP_CENTER': settings.DEFAULT_MAP_CENTER,
    }
    return render(template_name='signup.html', context=data, request=request)