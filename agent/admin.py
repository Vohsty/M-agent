from django.contrib import admin
from .models import *
from django import forms

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# from django.contrib.auth.admin import UserAdmin
# admin.site.register(CustomUserModel, UserAdmin)

admin.site.register(Building)
admin.site.register(House)
admin.site.register(Landlord)

class UserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length =30,label='Username')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name','password1', 'password2','username')}
        ),
    )

class LandAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name','password1', 'password2','username')}
        ),
    )



admin.site.register(User, UserAdmin,)
