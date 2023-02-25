from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.api.urls')),
    path('music/', include('music.api.urls')),
    path('playlist/', include('play_list.api.urls')),
]
