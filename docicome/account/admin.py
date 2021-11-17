from django.contrib import admin
from .models import Account, Doctor, Expertise, Order


@admin.register(Account)
class AuthorAdmin(admin.ModelAdmin):
    fields = Account.get_fields()
    list_display = Account.get_fields()


@admin.register(Doctor)
class AuthorAdmin(admin.ModelAdmin):
    list_display = Doctor.get_fields()


admin.site.register(Expertise)
admin.site.register(Order)
