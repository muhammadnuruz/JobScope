from django.contrib import admin
from .models import Companies


@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'ball', 'group_id', 'manager_count', 'employee_count',
        'is_approved', 'created_at'
    )
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'group_id', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    filter_horizontal = ('managers', 'employees')

    fieldsets = (
        ('📌 Основная информация', {
            'fields': ('name', 'description', 'link', 'ball', 'group_id')
        }),
        ('👥 Персонал', {
            'fields': ('managers', 'employees')
        }),
        ('⚙️ Статус модерации', {
            'fields': ('is_approved',)
        }),
        ('⏱️ Временные метки', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def manager_count(self, obj):
        return obj.managers.count()

    manager_count.short_description = "Кол-во менеджеров"

    def employee_count(self, obj):
        return obj.employees.count()

    employee_count.short_description = "Кол-во сотрудников"

    class Media:
        css = {
            'all': ('admin/custom_admin.css',)
        }
