from django.contrib import admin
from .models import Receita


class ListandoReceitas(admin.ModelAdmin):
    list_display = ('id', 'nome_receita', 'categoria', 'publicado')
    list_display_links = ('id', 'nome_receita')#fazendo esses campos se tornarem links
    search_fields = ('nome_receita',)
    list_filter = ('categoria',)
    list_editable = ('publicado',)
    list_per_page = 3

admin.site.register(Receita, ListandoReceitas)