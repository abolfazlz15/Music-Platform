from django.urls import path

from settings.api import views

urlpatterns = [
    path('detail/', views.SettingDetailView.as_view(), name='settings_detail'),
]