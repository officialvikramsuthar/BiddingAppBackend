

from django.contrib import admin
from UserProfile.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'mobile', 'is_active']


admin.site.register(User, UserAdmin)

