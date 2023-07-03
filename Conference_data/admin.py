from django.contrib import admin
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
    conf_s_desc = forms.CharField(
        label='Краткое описание',
        required=False,
        widget=CKEditorWidget(config_name='default'))
    conf_desc = forms.CharField(
        label='Полное описание',
        widget=CKEditorWidget(config_name='default'))
    conf_id = forms.CharField(disabled=True, required=False, help_text='Генерируется автоматически')

    class Meta:
        model = Conference
        fields = ('un_name', 'local', 'reg_date_begin', 'reg_date_end',
                  'conf_date_begin', 'conf_date_end', 'conf_card_href', 'reg_href',
                  'conf_name', 'conf_s_desc', 'conf_desc', 'org_name', 'themes',
                  'online', 'conf_href', 'offline', 'conf_address', 'contacts', 'rinc',
                  'checked', 'tags', 'conf_id',)


class ConferenceAdmin(admin.ModelAdmin):
    form = ConferenceAdminForm
    list_display = ['conf_name', 'conf_date_begin', 'checked']
    search_fields = ['conf_name']
    list_filter = ['conf_date_begin', 'checked']


admin_site.register(Conference, ConferenceAdmin)
admin_site.register(Tag)
