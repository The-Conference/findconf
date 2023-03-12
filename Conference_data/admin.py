from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.admin import AdminSite
from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Conference, Tag


class MyAdminSite(admin.AdminSite):
    site_header = 'TheConf'


admin_site = MyAdminSite(name='myadmin')
admin.site = admin_site


class ConferenceAdminForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    conf_s_desc = forms.CharField(label='Краткое описание', widget=CKEditorWidget(config_name='default'))
    conf_desc = forms.CharField(label='Полное описание', widget=CKEditorWidget(config_name='default'))

    class Meta:
        model = Conference
        fields = ('conf_id', 'hash', 'un_name', 'local', 'reg_date_begin', 'reg_date_end',
                  'conf_date_begin', 'conf_date_end', 'conf_card_href', 'reg_href',
                  'conf_name', 'conf_s_desc', 'conf_desc', 'org_name', 'themes',
                  'online', 'conf_href', 'offline', 'conf_address', 'contacts', 'rinc',
                  'checked', 'tags')


class ConferenceAdmin(admin.ModelAdmin):
    form = ConferenceAdminForm
    list_display = ['conf_name', 'checked']
    search_fields = ['conf_name']


admin_site.register(Conference, ConferenceAdmin)
admin_site.register(Tag)
# admin.site.unregister(User)
# admin.site.unregister(Group)
