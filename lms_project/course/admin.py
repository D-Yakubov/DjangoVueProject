from django.contrib import admin

from .models import Category, Course, Lesson, Comment, Quiz

class LessonCommentInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ['lesson']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'status', 'lesson_type', 'short_description']
    list_filter = ['status', 'lesson_type']
    search_fields = ['title', 'short_description', 'long_description']
    inlines = [LessonCommentInline]

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'content', 'lesson', 'created_at', 'created_by']
    list_filter = ['created_at', 'lesson__course']
    search_fields = ['name', 'content', 'created_by__username']

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Quiz)