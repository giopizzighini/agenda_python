from django.contrib import admin
from core.models import evento

# Register your models here.


class eventoadmin(admin.ModelAdmin):
    list_display = ("id","titulo","data_evento","data_criacao")
    list_filter = ("titulo","data_evento",)

admin.site.register(evento,eventoadmin)
