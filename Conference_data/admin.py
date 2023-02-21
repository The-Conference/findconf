from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Conference, Tag

admin.site.register(Conference)
admin.site.register(Tag)
admin.site.unregister(User)
admin.site.unregister(Group)
