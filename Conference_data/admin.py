from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from ckeditor.widgets import CKEditorWidget

from .models import Conference, Tag, Grant


class MyAdminSite(admin.AdminSite):
    site_header = 'TheConf'


admin_site = MyAdminSite(name='myadmin')
admin.site = admin_site


class ConferenceAdminForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by('name'),
        required=False,
        widget=FilteredSelectMultiple(verbose_name='Тэги', is_stacked=False),
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
                  'vak', 'wos', 'scopus', 'checked', 'tags', 'conf_id',)


class ConferenceAdmin(admin.ModelAdmin):
    form = ConferenceAdminForm
    list_display = ['conf_name', 'conf_date_begin', 'checked']
    search_fields = ['conf_name']
    list_filter = ['conf_date_begin', 'checked']
    fieldsets = (
        (None, {
            'fields': ('conf_name', 'un_name')
        }),
        ('Характеристики', {
            'fields': [('local', 'online', 'offline', 'checked')],
        }),
        ('Даты', {
            'fields': [('conf_date_begin', 'conf_date_end'), ('reg_date_begin', 'reg_date_end')],
        }),
        ('Тексты', {
            'fields': ('conf_s_desc', 'conf_desc', 'conf_address', 'contacts'),
        }),
        ('Ссылки', {
            'fields': ('conf_card_href', 'reg_href', 'conf_href'),
        }),
        ('Системы цитирования', {
            'fields': [('rinc', 'vak', 'wos', 'scopus')],
        }),
        ('Тэги', {
            'fields': ('tags', ),
        }),
        ('Разное', {
            'classes': ['collapse'],
            'fields': ('org_name', 'themes', 'conf_id'),
        }),
    )


class GrantAdminForm(ConferenceAdminForm):
    class Meta:
        model = Grant
        fields = ('un_name', 'local', 'reg_date_begin', 'reg_date_end',
                  'conf_card_href', 'reg_href', 'conf_name', 'conf_s_desc', 'conf_desc',
                  'contacts', 'checked', 'tags', 'conf_id',)


class GrantAdmin(admin.ModelAdmin):
    form = GrantAdminForm
    list_display = ['conf_name', 'checked']
    search_fields = ['conf_name']
    list_filter = ['checked']


admin_site.register(Conference, ConferenceAdmin)
admin_site.register(Grant, GrantAdmin)
admin_site.register(Tag)
