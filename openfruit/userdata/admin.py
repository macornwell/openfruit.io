from django.contrib import admin
from openfruit.userdata.models import UserProfile
from openfruit.userdata.forms import UserProfileForm


class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm

admin.site.register(UserProfile, UserProfileAdmin)
