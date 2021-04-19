# app retirado de uso na parte 4 do curso da Alura
from django.db import models

class Pessoas(models.Model):
    nome = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):#fazendo o nome das pessoas aparecerem no admin das receitas
        return self.nome