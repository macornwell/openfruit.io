from django.contrib import admin
from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField
from openfruit.common.services import is_curator
from openfruit.common.models import UserProfile, Signup

admin.site.register(UserProfile)
admin.site.register(Signup)

class FilterUserAdmin(admin.ModelAdmin):
    """
    Filters out all objects unless the user created them, or they have the
    appropriate permissions.
    """
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(FilterUserAdmin, self).get_queryset(request)
        return qs.filter(submitted_by=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser:
            return True
        elif is_curator(request.user):
            return True
        elif obj.submitted_by is request.user:
            return True
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'submitted_by':
            kwargs['initial'] = request.user
            queryset = User.objects.filter(id=request.user.id)
            return ModelChoiceField(queryset, initial=request.user)
        return super(FilterUserAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )



