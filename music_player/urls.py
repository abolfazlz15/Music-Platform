from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.api.urls')),
    path('music/', include('music.api.urls')),
    path('playlist/', include('play_list.api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
