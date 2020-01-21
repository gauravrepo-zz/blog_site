from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('username','first_name', 'last_name', 'email', 'date_joined','last_login','is_admin')
    sear_fields = ('username','first_name', 'last_name', 'email')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
admin.site.register(Account, AccountAdmin)