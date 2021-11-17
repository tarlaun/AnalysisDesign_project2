from django.contrib import admin
from django.contrib.admin.decorators import display
from django.contrib.auth.admin import UserAdmin
from .forms import AccountCreationForm 
from .models import Account, Doctor


@admin.register(Account)
class AccountAdmin(UserAdmin):
   
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', "phone_number")
        }),
         
        ('Additional info', {
            'fields': ('user_type', )
        })
    )
    list_display = Account.get_fields()
    
     
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = Doctor.get_fields()
