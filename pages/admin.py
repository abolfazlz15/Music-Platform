from django.contrib import admin
from pages.models import TicketTitle, Ticket, AboutUs


admin.site.register(TicketTitle)
admin.site.register(AboutUs)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'get_jalali_date']
    list_filter = ['created_at']
    search_fields = ['title', 'user']
    list_select_related = ['title', 'user']