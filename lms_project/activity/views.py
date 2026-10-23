from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from course.models import Course, Lesson
from course.serializers import CourseListSerializer

from .models import Activity
from .serializers import ActivitySerializer


@api_view(['GET'])
def get_active_courses(request):
    courses = (
        Course.objects.filter(
            status=Course.PUBLISHED,
            activities__created_by=request.user,
            activities__status=Activity.STARTED,
        )
        .distinct()
    )

    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def track_started(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, status=Course.PUBLISHED)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug, status=Lesson.PUBLISHED)

    activity = Activity.objects.filter(
        created_by=request.user,
        course=course,
        lesson=lesson,
    ).first()

    if not activity:
        activity = Activity.objects.create(
            course=course,
            lesson=lesson,
            created_by=request.user,
            status=Activity.STARTED,
        )

    serializer = ActivitySerializer(activity)
    return Response(serializer.data)


@api_view(['POST'])
def mark_as_done(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, status=Course.PUBLISHED)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug, status=Lesson.PUBLISHED)

    activity = Activity.objects.filter(
        created_by=request.user,
        course=course,
        lesson=lesson,
    ).first()

    if not activity:
        activity = Activity.objects.create(
            course=course,
            lesson=lesson,
            created_by=request.user,
            status=Activity.DONE,
        )
    else:
        activity.status = Activity.DONE
        activity.save(update_fields=['status'])

    serializer = ActivitySerializer(activity)
    return Response(serializer.data)
