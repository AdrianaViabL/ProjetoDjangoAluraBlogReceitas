from django.contrib import admin
from .models import Pessoas


class VerPessoas(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')
    list_display_links = ('id', 'nome',)

admin.site.register(Pessoas, VerPessoas)