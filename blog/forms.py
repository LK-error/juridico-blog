# blog/forms.py
 
from django import forms
from .models import Categoria
from ckeditor_uploader.widgets import CKEditorUploadingWidget
 
 # Definimos as opções de escolha para o tipo de conteúdo
TIPO_CONTEUDO_CHOICES = [
  ('artigo', 'Artigo Interno'),
  ('link', 'Link Externo'),
 ]
 
class ConteudoForm(forms.Form):
  # O campo para escolher entre Artigo e Link. Usará botões de rádio.
  tipo_conteudo = forms.ChoiceField(
  choices=TIPO_CONTEUDO_CHOICES,
  widget=forms.RadioSelect,
  initial='artigo', # Começa pré-selecionado como 'Artigo Interno'
  label="Qual tipo de conteúdo você quer criar?"
  )
 
  # --- Campos comuns a ambos os tipos ---
  titulo = forms.CharField(
  max_length=200,
  widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Digite o título aqui'})
  )
  categoria = forms.ModelChoiceField(
  queryset=Categoria.objects.all(),
  widget=forms.Select(attrs={'class': 'form-select'}),
  empty_label="Selecione uma categoria"
  )
 
  # --- Campo exclusivo para Artigo Interno ---
  conteudo = forms.CharField(
  widget=CKEditorUploadingWidget(), # <--- A MUDANÇA IMPORTANTE ESTÁ AQUI
  required=False # Não é obrigatório, pois pode ser um link
  )
 
  # --- Campos exclusivos para Link Externo ---
  link_url = forms.URLField(
  max_length=500,
  widget=forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://exemplo.com'}),
  required=False, # Não é obrigatório, pois pode ser um artigo
  label="Link (URL)"
  )
  resumo = forms.CharField(
  widget=CKEditorUploadingWidget(), # <--- A MUDANÇA IMPORTANTE ESTÁ AQUI
  required=False # Não é obrigatório, pois pode ser um artigo
    )