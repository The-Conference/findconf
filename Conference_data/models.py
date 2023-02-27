from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return f'{self.name}'


class Conference(models.Model):
    conf_id = models.TextField(unique=True)
    hash = models.CharField(max_length=500)
    un_name = models.CharField(max_length=500, verbose_name="ВУЗ")
    local = models.BooleanField()
    reg_date_begin = models.DateField(null=True, blank=True, verbose_name="Начало регистрации")
    reg_date_end = models.DateField(null=True, blank=True, verbose_name="Окончание регистрации")
    conf_date_begin = models.DateField(null=True, blank=True, verbose_name="Дата начала")
    conf_date_end = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    conf_card_href = models.URLField(max_length=500, blank=True, verbose_name="Карточка конференции")
    reg_href = models.URLField(max_length=500, blank=True, verbose_name="Ссылка на регистрацию")
    conf_name = models.TextField(blank=True, verbose_name="Название")
    conf_s_desc = models.TextField(blank=True, verbose_name="Краткое описание")
    conf_desc = models.TextField(blank=True, verbose_name="Описание")
    org_name = models.TextField(blank=True, verbose_name="Организатор")
    themes = models.TextField(blank=True, verbose_name="Тематика (от организатора)")
    online = models.BooleanField()
    conf_href = models.URLField(max_length=500, blank=True, verbose_name="Ссылка")
    offline = models.BooleanField()
    conf_address = models.TextField(blank=True, verbose_name="Адрес")
    contacts = models.TextField(blank=True, verbose_name="Контакты")
    rinc = models.BooleanField(verbose_name="РИНЦ")
    data = models.JSONField()
    checked = models.BooleanField(default=False, verbose_name="Проверено")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")

    @property
    def conf_status(self):
        current_date = timezone.now().date()
        if self.conf_date_begin <= current_date <= self.conf_date_end:
            return "ongoing"
        else:
            return "upcoming" if self.conf_date_begin > current_date else "past"

    class Meta:
        verbose_name = "Конференция"
        verbose_name_plural = "Конференции"

    def __str__(self):
        return f'{self.un_name} - {self.conf_name}'
