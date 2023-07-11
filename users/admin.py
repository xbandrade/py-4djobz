from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import ApplicantProfile, CustomUser


class ApplicantProfileForm(forms.ModelForm):
    phone_number = forms.IntegerField(
        required=False, widget=forms.TextInput(attrs={'type': 'number'}))

    class Meta:
        model = ApplicantProfile
        fields = '__all__'
        widgets = {
            'years_experience': forms.NumberInput(attrs={'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class ApplicantProfileInline(admin.StackedInline):
    model = ApplicantProfile
    form = ApplicantProfileForm
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = [ApplicantProfileInline]
    list_display = (
        'email', 'full_name', 'phone_number', 'is_staff', 'is_company')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)
    form = ApplicantProfileForm

    def full_name(self, obj):
        return (f'{obj.applicantprofile.first_name} '
                f'{obj.applicantprofile.last_name}'
                if not obj.is_company else f'{obj.companyprofile.name}')

    full_name.short_description = _('Name')


admin.site.register(CustomUser, CustomUserAdmin)
