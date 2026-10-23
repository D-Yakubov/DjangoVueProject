from django.contrib import admin

from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['course', 'lesson', 'created_by', 'status', 'created_at']
    list_filter = ['status', 'course', 'created_at']
    search_fields = ['course__title', 'lesson__title', 'created_by__username']
