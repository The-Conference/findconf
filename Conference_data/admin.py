from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

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
    short_description = forms.CharField(
        label='Краткое описание',
        required=False,
        widget=forms.Textarea(attrs={'rows': '10', 'cols': '80'}))
    description = forms.CharField(
        label='Полное описание',
        widget=CKEditorWidget(config_name='default'))
    item_id = forms.CharField(disabled=True, required=False, help_text='Генерируется автоматически')

    class Meta:
        model = Conference
        fields = ('un_name', 'local', 'reg_date_begin', 'reg_date_end',
                  'conf_date_begin', 'conf_date_end', 'source_href', 'reg_href',
                  'title', 'short_description', 'description', 'org_name', 'themes',
                  'online', 'conf_href', 'offline', 'conf_address', 'contacts', 'rinc',
                  'vak', 'wos', 'scopus', 'checked', 'tags', 'item_id',)


class ConferenceAdmin(admin.ModelAdmin):
    form = ConferenceAdminForm
    list_display = ['title', 'conf_date_begin', 'checked']
    search_fields = ['title']
    list_filter = ['conf_date_begin', 'checked']
    fieldsets = (
        (None, {
            'fields': ('title', 'un_name')
        }),
        ('Характеристики', {
            'fields': [('local', 'online', 'offline', 'checked')],
        }),
        ('Даты', {
            'fields': [('conf_date_begin', 'conf_date_end'), ('reg_date_begin', 'reg_date_end')],
        }),
        ('Тексты', {
            'fields': ('short_description', 'description', 'conf_address', 'contacts'),
        }),
        ('Ссылки', {
            'fields': ('source_href', 'reg_href', 'conf_href'),
        }),
        ('Системы цитирования', {
            'fields': [('rinc', 'vak', 'wos', 'scopus')],
        }),
        ('Тэги', {
            'fields': ('tags', ),
        }),
        ('Разное', {
            'classes': ['collapse'],
            'fields': ('org_name', 'themes', 'item_id'),
        }),
    )


class GrantAdminForm(ConferenceAdminForm):
    class Meta:
        model = Grant
        fields = ('un_name', 'local', 'reg_date_begin', 'reg_date_end',
                  'source_href', 'reg_href', 'title', 'short_description', 'description',
                  'contacts', 'checked', 'tags', 'item_id',)


class GrantAdmin(admin.ModelAdmin):
    form = GrantAdminForm
    list_display = ['title', 'reg_date_end', 'checked']
    search_fields = ['title']
    list_filter = ['reg_date_end', 'checked']
    fieldsets = (
        (None, {
            'fields': ('title', 'un_name')
        }),
        ('Характеристики', {
            'fields': [('local', 'checked')],
        }),
        ('Даты', {
            'fields': [('reg_date_begin', 'reg_date_end')],
        }),
        ('Тексты', {
            'fields': ('short_description', 'description', 'contacts'),
        }),
        ('Ссылки', {
            'fields': ('source_href', 'reg_href'),
        }),
        ('Тэги', {
            'fields': ('tags', ),
        }),
        ('Разное', {
            'classes': ['collapse'],
            'fields': ('item_id', ),
        }),
    )


admin_site.register(Conference, ConferenceAdmin)
admin_site.register(Grant, GrantAdmin)
admin_site.register(Tag)
