from django.contrib import admin
from .models import Debt


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ("borrower_name", "amount", "deadline", "user", "created_at")
    search_fields = ("borrower_name", "user__full_name")
    list_filter = ("deadline",)
