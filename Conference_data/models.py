from django.db import models


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
    un_name = models.CharField(max_length=500)
    local = models.BooleanField()
    reg_date_begin = models.CharField(max_length=500, blank=True)
    reg_date_end = models.CharField(max_length=500, blank=True)
    conf_date_begin = models.CharField(max_length=500, blank=True)
    conf_date_end = models.CharField(max_length=500, blank=True)
    conf_card_href = models.URLField(max_length=500, blank=True)
    reg_href = models.URLField(max_length=500, blank=True)
    conf_name = models.TextField(blank=True)
    conf_s_desc = models.TextField(blank=True)
    conf_desc = models.TextField(blank=True)
    org_name = models.TextField(blank=True)
    themes = models.TextField(blank=True)
    online = models.BooleanField()
    conf_href = models.URLField(max_length=500, blank=True)
    offline = models.BooleanField()
    conf_address = models.TextField(blank=True)
    contacts = models.TextField(blank=True)
    rinc = models.BooleanField()
    data = models.JSONField()
    checked = models.BooleanField(default=False, verbose_name="Проверено контент-менеджером")
    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name = "Конференция"
        verbose_name_plural = "Конференции"

    def __str__(self):
        return f'{self.un_name} - {self.conf_name}'
