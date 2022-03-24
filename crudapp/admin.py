from django.contrib import admin
from crudapp.models import *
# Register your models here.

admin.site.register(Person)
admin.site.register(Todo)
admin.site.register(User)
admin.site.register(ItemsList)