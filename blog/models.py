# blog/models.py

from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Artigo(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = RichTextUploadingField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.titulo

class LinkExterno(models.Model):
    titulo = models.CharField(max_length=200)
    link_url = models.URLField(max_length=500)
    resumo = RichTextUploadingField(help_text="Adicione um breve comentário ou resumo sobre o link.")
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titulo

# NOVO MODELO (local correto do campo 'area_atuacao')
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    area_atuacao = models.CharField(max_length=200, help_text="Ex: Cível e Família")
    bio = models.TextField(blank=True, help_text="Uma breve biografia ou descrição profissional.")

    def __str__(self):
        return self.usuario.username