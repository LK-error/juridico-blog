# intranet_flores/urls.py

from django.contrib import admin
from django.urls import path, include  # 'include' é crucial aqui
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # Esta linha deve aparecer APENAS UMA VEZ
    # Ela direciona todo o tráfego do site para o arquivo de URLs do app 'blog'
    path('', include('blog.urls')), 
]

# Esta parte é para servir as imagens durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)