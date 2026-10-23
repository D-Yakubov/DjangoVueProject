from django.contrib import admin

from .models import Category, Comment, Course, Lesson, Quiz


class LessonCommentInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ['lesson']
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'status', 'created_at']
    list_filter = ['status', 'categories', 'created_at']
    search_fields = ['title', 'short_description', 'long_description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'status', 'lesson_type']
    list_filter = ['status', 'lesson_type', 'course']
    search_fields = ['title', 'short_description', 'long_description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonCommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'lesson', 'created_by', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['name', 'content']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['question', 'lesson', 'answer']
    list_filter = ['lesson__course']
    search_fields = ['question']
