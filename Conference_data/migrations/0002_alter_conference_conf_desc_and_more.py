# Generated by Django 4.1.6 on 2023-03-12 15:31

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Conference_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='conf_desc',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_s_desc',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Краткое описание'),
        ),
    ]
