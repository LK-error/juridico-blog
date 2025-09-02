# blog/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Artigo, Categoria, LinkExterno, Perfil # Importe o Perfil

# Define um "inline" para o modelo de Perfil
# Isso permite que o Perfil seja editado na mesma página que o Usuário
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfis'

# Define uma nova classe de Admin para o Usuário
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

# Desregistra o User Admin padrão e registra o nosso personalizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Registra os outros modelos como antes
admin.site.register(Artigo)
admin.site.register(Categoria)
admin.site.register(LinkExterno)