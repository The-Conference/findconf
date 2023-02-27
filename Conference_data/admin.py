from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.admin import AdminSite

from .models import Conference, Tag


class MyAdminSite(admin.AdminSite):
    site_header = 'TheConf'


admin_site = MyAdminSite(name='myadmin')
admin.site = admin_site


class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['conf_name', 'checked']
    search_fields = ['conf_name']


admin_site.register(Conference, ConferenceAdmin)
admin_site.register(Tag)
# admin.site.unregister(User)
# admin.site.unregister(Group)
