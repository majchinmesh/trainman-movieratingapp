from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import Account
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email','username','date_joined', 'last_login', 'is_admin','is_staff')
    search_fields = ('email','username',)
    readonly_fields=('date_joined', 'last_login')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username', 'password1', 'password2'),
            }),
            )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
