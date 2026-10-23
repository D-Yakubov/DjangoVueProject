from random import randint

from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework import status as drf_status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from .models import Category, Comment, Course, Lesson
from .serializers import (
    CategorySerializer,
    CommentsSerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    LessonListSerializer,
    LessonPreviewSerializer,
    QuizSerializer,
    UserSerializer,
)


@api_view(['POST'])
def create_course(request):
    title = (request.data.get('title') or '').strip()
    if not title:
        return Response(
            {'error': 'Course title is required.'},
            status=drf_status.HTTP_400_BAD_REQUEST,
        )

    raw_status = request.data.get('status', Course.DRAFT)
    if raw_status in ('review', Course.IN_REVIEW):
        course_status = Course.IN_REVIEW
    else:
        course_status = Course.DRAFT

    with transaction.atomic():
        course = Course.objects.create(
            title=title,
            slug=f"{slugify(title)}-{randint(1000, 10000)}",
            short_description=request.data.get('short_description', ''),
            long_description=request.data.get('long_description', ''),
            status=course_status,
            created_by=request.user,
        )

        category_ids = request.data.get('categories') or []
        if isinstance(category_ids, list) and category_ids:
            valid_categories = Category.objects.filter(id__in=category_ids)
            course.categories.set(valid_categories)

        lessons_data = request.data.get('lessons') or []
        if isinstance(lessons_data, list):
            for lesson in lessons_data:
                lesson_title = (lesson.get('title') or '').strip()
                if not lesson_title:
                    continue
                Lesson.objects.create(
                    course=course,
                    title=lesson_title,
                    slug=slugify(lesson_title),
                    short_description=lesson.get('short_description', ''),
                    long_description=lesson.get('long_description', ''),
                    status=Lesson.DRAFT,
                )

    return Response({'course_id': course.id}, status=drf_status.HTTP_201_CREATED)


@api_view(['GET'])
def get_quiz(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, status=Course.PUBLISHED)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug, status=Lesson.PUBLISHED)
    quiz = lesson.quizzes.first()
    if not quiz:
        return Response({'detail': 'Quiz not found for this lesson.'}, status=drf_status.HTTP_404_NOT_FOUND)
    serializer = QuizSerializer(quiz)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_courses(request):
    category_id = request.GET.get('category_id', '').strip()
    courses = Course.objects.filter(status=Course.PUBLISHED)

    if category_id:
        try:
            courses = courses.filter(categories__id=int(category_id)).distinct()
        except ValueError:
            return Response(
                {'error': 'Invalid category_id parameter.'},
                status=drf_status.HTTP_400_BAD_REQUEST,
            )

    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_frontpage_courses(request):
    courses = Course.objects.filter(status=Course.PUBLISHED)[:4]
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def get_course(request, slug):
    course = get_object_or_404(
        Course.objects.select_related('created_by'),
        slug=slug,
        status=Course.PUBLISHED,
    )
    published_lessons = course.lessons.filter(status=Lesson.PUBLISHED)
    course_serializer = CourseDetailSerializer(course)

    if request.user.is_authenticated:
        lesson_serializer = LessonListSerializer(published_lessons, many=True)
    else:
        lesson_serializer = LessonPreviewSerializer(published_lessons, many=True)

    return Response({
        'course': course_serializer.data,
        'lessons': lesson_serializer.data,
    })


@api_view(['GET'])
def get_comments(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, status=Course.PUBLISHED)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug, status=Lesson.PUBLISHED)
    serializer = CommentsSerializer(lesson.comments.all(), many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_comment(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, status=Course.PUBLISHED)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug, status=Lesson.PUBLISHED)

    name = (request.data.get('name') or '').strip()
    content = (request.data.get('content') or '').strip()

    if not name or not content:
        return Response(
            {'error': 'Both name and content are required.'},
            status=drf_status.HTTP_400_BAD_REQUEST,
        )

    comment = Comment.objects.create(
        course=course,
        lesson=lesson,
        name=name,
        content=content,
        created_by=request.user,
    )

    serializer = CommentsSerializer(comment)
    return Response(serializer.data, status=drf_status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([])
def get_author_courses(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    courses = user.courses.filter(status=Course.PUBLISHED)

    user_serializer = UserSerializer(user, many=False)
    courses_serializer = CourseListSerializer(courses, many=True)

    return Response({
        'courses': courses_serializer.data,
        'created_by': user_serializer.data,
    })
