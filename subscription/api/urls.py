from django.urls import path
from subscription.api import views

urlpatterns = [
    path('list', views.MemberShipListView.as_view(), name='membership_list'),
]