# Generated by Django 4.1.6 on 2023-03-26 15:50

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conference_data', '0002_alter_conference_conf_desc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='conf_address',
            field=models.TextField(blank=True, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_card_href',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Карточка конференции'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_date_begin',
            field=models.DateField(verbose_name='Дата начала'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_desc',
            field=ckeditor.fields.RichTextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_href',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_name',
            field=models.TextField(verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_s_desc',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='contacts',
            field=models.TextField(blank=True, null=True, verbose_name='Контакты'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='hash',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='conference',
            name='local',
            field=models.BooleanField(default=True, verbose_name='Международная'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='offline',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='conference',
            name='online',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='conference',
            name='org_name',
            field=models.TextField(blank=True, null=True, verbose_name='Организатор'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='reg_href',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Ссылка на регистрацию'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='rinc',
            field=models.BooleanField(default=False, verbose_name='РИНЦ'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='themes',
            field=models.TextField(blank=True, null=True, verbose_name='Тематика (от организатора)'),
        ),
    ]