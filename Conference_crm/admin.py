from django.contrib import admin
from django.contrib.auth.models import Group

from Conference_crm.models import User

# Register your models here.
admin.site.register(User)
admin.site.register(Group)
