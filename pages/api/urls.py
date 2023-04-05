from django.urls import path

from pages.api import views

app_name = 'page'
urlpatterns = [
    path('ticket', views.CreateTicketView.as_view(), name='create_ticket'),
    path('ticket-title', views.TicketTitleListView.as_view(), name='ticket_title_list'),


]
