from django.db import models
from auditlog.registry import auditlog
from openfruit.common.models import IntegerRangeField


class GeoCoordinate(models.Model):
    geocoordinate_id = models.AutoField(primary_key=True)
    lat_integer = IntegerRangeField(min_value=-89, max_value=89)
    lat_fractional = models.IntegerField()
    lon_integer = IntegerRangeField(min_value=-179, max_value=179)
    lon_fractional = models.IntegerField()

    def __str__(self):
        return '{0}.{1} {2}.{3}'.format(self.lat_integer, self.lat_fractional, self.lon_integer, self.lon_fractional)

    def save(self, *args, **kwargs):
        self.__standardize_fractionals()
        super(GeoCoordinate, self).save(*args, **kwargs)

    @staticmethod
    def get_standardized(latOrLon):
        objInt, objFrac = latOrLon.split('.', 1)
        objFrac = int(str(objFrac)[0:5])
        objFrac = int('{0:05d}'.format(objFrac))
        return (objInt, objFrac)

    def __standardize_fractionals(self):
        latFrac = str(self.lat_fractional)[0:5]
        lonFrac = str(self.lon_fractional)[0:5]
        latFrac = '{0:05d}'.format(int(latFrac))
        lonFrac = '{0:05d}'.format(int(lonFrac))
        self.lat_fractional = latFrac
        self.lon_fractional = lonFrac

    class Meta:
        unique_together = ('lat_integer', 'lat_fractional', 'lon_integer', 'lon_fractional')


class Continent(models.Model):
    continent_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    continent = models.ForeignKey(Continent)
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=2, unique=True)
    geocoordinate = models.ForeignKey(GeoCoordinate)


class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=2, unique=True)
    geocoordinate = models.ForeignKey(GeoCoordinate)

    class Meta:
        unique_together = (('country', 'name'),)

    def __str__(self):
        return self.name


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    state = models.ForeignKey(State)
    name = models.CharField(max_length=50)
    geocoordinate = models.ForeignKey(GeoCoordinate)

    class Meta:
        unique_together = (('state', 'name'),)

    def __str__(self):
        return '{0}, {1}'.format(self.name, self.state.name)


class Zipcode(models.Model):
    us_zipcode_id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City)
    zipcode = IntegerRangeField(unique=True, min_value=1, max_value=99999)
    geocoordinate = models.ForeignKey(GeoCoordinate)

    class Meta:
        unique_together = ('zipcode', 'geocoordinate')


class Location(models.Model):
    """
    The working horse of locational data.
    This is the object that should be a foreign key to MOST geolocated objects.
    It is a cascading of Locational information that gets more detailed depending on
    what level of granularity is desired, the minimum being a country.
    """
    location_id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country)
    state = models.ForeignKey(State, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)
    zipcode = models.ForeignKey(Zipcode, blank=True, null=True)
    geocoordinate = models.ForeignKey(GeoCoordinate, blank=True, null=True, help_text='This is a very specific location.')
    name = models.CharField(max_length=30, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.state and self.state.country != self.country:
            raise Exception("The state's country does not match the selected country.")
        if self.city and self.city.state != self.state:
            raise Exception("City's state does not match the selected state.")
        if self.zipcode and self.zipcode.city != self.city:
            raise Exception("Zipcode's city does not match the selected city.")
        super(Location, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('country', 'state', 'city', 'zipcode', 'geocoordinate')





auditlog.register(Continent)
auditlog.register(Country)
auditlog.register(City)
auditlog.register(State)
auditlog.register(Location)
auditlog.register(Zipcode)
