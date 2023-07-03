from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField


class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return f'{self.name}'


class Conference(models.Model):
    conf_id = models.TextField(unique=True)
    hash = models.CharField(null=True, blank=True, max_length=500)  # Legacy code, deprecated
    un_name = models.CharField(max_length=500, verbose_name="ВУЗ")
    local = models.BooleanField(default=True, verbose_name="Международная")
    reg_date_begin = models.DateField(null=True, blank=True, verbose_name="Начало регистрации")
    reg_date_end = models.DateField(null=True, blank=True, verbose_name="Окончание регистрации")
    conf_date_begin = models.DateField(verbose_name="Дата начала")
    conf_date_end = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    conf_card_href = models.URLField(null=True, blank=True, max_length=500, verbose_name="Карточка конференции")
    reg_href = models.URLField(null=True, blank=True, max_length=500, verbose_name="Ссылка на регистрацию")
    conf_name = models.TextField(verbose_name="Название")
    conf_s_desc = RichTextField(null=True, blank=True, verbose_name="Краткое описание")
    conf_desc = RichTextField(verbose_name="Описание")
    org_name = models.TextField(null=True, blank=True, verbose_name="Организатор")
    themes = models.TextField(null=True, blank=True, verbose_name="Тематика (от организатора)")
    online = models.BooleanField(default=False)
    conf_href = models.URLField(null=True, blank=True, max_length=500, verbose_name="Ссылка")
    offline = models.BooleanField(default=True)
    conf_address = models.TextField(null=True, blank=True, verbose_name="Адрес")
    contacts = models.TextField(null=True, blank=True, verbose_name="Контакты")
    rinc = models.BooleanField(default=False, verbose_name="РИНЦ")
    data = models.JSONField(blank=True, null=True)
    checked = models.BooleanField(default=False, verbose_name="Проверено")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")

    generate_conf_id = models.BooleanField(default=False)  # Legacy code, deprecated

    vak = models.BooleanField(default=False)
    wos = models.BooleanField(default=False)
    scopus = models.BooleanField(default=False)

    def clean(self) -> None:
        """Validate_unique is needed to show an error in admin,
        otherwise it fails with error 500."""
        if not self.conf_id:
            self.conf_id = f"{self.un_name[:100]}{self.conf_name[:100]}{self.conf_date_begin}"
        self.validate_unique()

    def save(self, *args, **kwargs):
        self.conf_s_desc = self.normalize(self.conf_s_desc)
        self.conf_desc = self.normalize(self.conf_desc)
        self.clean()
        super().save(*args, **kwargs)

    @staticmethod
    def normalize(string: str) -> str:
        if string:
            string.replace('\n', '').replace('\t', '')
        return string

    @property
    def conf_status(self) -> str:
        current_date = timezone.now().date()
        if self.conf_date_begin is None or self.conf_date_end is None:  # TODO: Delete?
            return "Дата уточняется"
        elif self.conf_date_begin <= current_date <= self.conf_date_end:
            return "Конференция идёт"
        elif (self.conf_date_begin - current_date).days <= 14 and current_date < self.conf_date_begin:
            return "Конференция скоро начнётся"
        elif self.conf_date_begin > current_date:
            return "Конференция запланирована"
        else:
            return "Конференция окончена"

    class Meta:
        verbose_name = "Конференция"
        verbose_name_plural = "Конференции"

    def __str__(self):
        return f'{self.un_name} - {self.conf_name}'
