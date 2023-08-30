from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField

from Conference_crm.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return f'{self.name}'


class AbstractItem(models.Model):
    conf_id = models.TextField(unique=True)
    un_name = models.CharField(max_length=500, verbose_name="ВУЗ")
    local = models.BooleanField(default=True, verbose_name="Международная")
    reg_date_begin = models.DateField(null=True, blank=True, verbose_name="Начало регистрации")
    reg_date_end = models.DateField(null=True, blank=True, verbose_name="Окончание регистрации")
    conf_card_href = models.URLField(null=True, blank=True, max_length=500, verbose_name="Ссылка на источник")
    reg_href = models.URLField(null=True, blank=True, max_length=500, verbose_name="Ссылка на регистрацию")
    conf_name = models.TextField(verbose_name="Название")
    conf_s_desc = RichTextField(null=True, blank=True, verbose_name="Краткое описание")
    conf_desc = RichTextField(verbose_name="Описание")
    contacts = models.TextField(null=True, blank=True, verbose_name="Контакты")
    checked = models.BooleanField(default=False, verbose_name="Проверено")

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.un_name} - {self.conf_name}'

    def clean(self) -> None:
        """Validate_unique is needed to show an error in admin,
        otherwise it fails with error 500."""
        self.conf_id = self.conf_id.replace(' ', '')
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


class Conference(AbstractItem):
    hash = models.CharField(null=True, blank=True, max_length=500)  # Legacy code, deprecated
    conf_date_begin = models.DateField(verbose_name="Дата начала")
    conf_date_end = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    org_name = models.TextField(null=True, blank=True, verbose_name="Организатор")
    themes = models.TextField(null=True, blank=True, verbose_name="Тематика (от организатора)")
    online = models.BooleanField(default=False, verbose_name="Онлайн")
    conf_href = models.URLField(null=True, blank=True, max_length=500, verbose_name="Сайт конференции")
    offline = models.BooleanField(default=True, verbose_name="Оффлайн")
    conf_address = models.TextField(null=True, blank=True, verbose_name="Адрес")
    rinc = models.BooleanField(default=False, verbose_name="РИНЦ")
    data = models.JSONField(blank=True, null=True)  # Legacy code, deprecated
    generate_conf_id = models.BooleanField(default=False)  # Legacy code, deprecated
    vak = models.BooleanField(default=False, verbose_name="ВАК")
    wos = models.BooleanField(default=False, verbose_name="WoS")
    scopus = models.BooleanField(default=False, verbose_name="Scopus")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    favorites = GenericRelation('Favorite')

    def clean(self) -> None:
        if not self.conf_id:
            self.conf_id = f"{self.un_name[:100]}{self.conf_name[:100]}{self.conf_date_begin}"
        super().clean()

    @property
    def conf_status(self) -> str:
        current_date = timezone.now().date()
        if self.conf_date_end is None:
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


class Grant(AbstractItem):
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    favorites = GenericRelation('Favorite')

    class Meta:
        verbose_name = "Грант"
        verbose_name_plural = "Гранты"

    def clean(self) -> None:
        if not self.conf_id:
            self.conf_id = f"{self.un_name[:100]}{self.conf_name[:100]}{self.reg_date_end}"
        super().clean()


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'object_id', 'content_type'],
                name='unique_user_content_type_object_id'
            )
        ]
