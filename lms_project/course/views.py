from random import randint

from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.text import slugify
from rest_framework import serializers

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson, Comment, Category, Quiz
from .serializers import CourseListSerializer, CourseDetailSerializer, LessonListSerializer, CommentsSerializer, CategorySerializer, QuizSerializer, UserSerializer, QuizQuestionSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course(request):
    status = request.data.get('status')

    print(request.data)

    if status == 'published':
        status = 'draft'

    course = Course.objects.create(
        title=request.data.get('title'),
        slug='%s-%s' % (slugify(request.data.get('title')), randint(1000, 10000)),
        short_description=request.data.get('short_description'),
        long_description=request.data.get('long_description'),
        status=status,
        created_by=request.user
    )

    for id in request.data.get('categories'):
        course.categories.add(id)
    
    course.save()

    # Lessons

    for lesson in request.data.get('lessons'):
        tmp_lesson = Lesson.objects.create(
            course=course,
            title=lesson.get('title'),
            slug=slugify(lesson.get('title')),
            short_description=lesson.get('short_description'),
            long_description=lesson.get('long_description'),
            status=Lesson.DRAFT
        )

    return Response({'course_id': course.id})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quiz_questions(request, course_slug, lesson_slug):
    lesson = Lesson.objects.get(slug=lesson_slug)
    questions = lesson.quizzes.all()
    serializer = QuizQuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_courses(request):
    category_id = request.GET.get('category_id', '')
    courses = Course.objects.filter(status=Course.PUBLISHED)

    if category_id:
        courses = courses.filter(categories__in=[int(category_id)])

    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_frontpage_courses(request):
    courses = Course.objects.filter(status=Course.PUBLISHED)[0:4]
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course(request, slug):
    course = Course.objects.filter(status=Course.PUBLISHED).get(slug=slug)
    course_serializer = CourseDetailSerializer(course)
    lesson_serializer = LessonListSerializer(course.lessons.all(), many=True)

    return Response({
        'course': course_serializer.data,
        'lessons': lesson_serializer.data
    })

@api_view(['GET'])
def get_comments(request, course_slug, lesson_slug):
    lesson = Lesson.objects.get(slug=lesson_slug)
    serializer = CommentsSerializer(lesson.comments.all(), many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_comment(request, course_slug, lesson_slug):
    data = request.data
    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug)

    comment = Comment.objects.create(course=course, lesson=lesson, name=data.get('name'), content=data.get('content'), created_by=request.user)

    serializer = CommentsSerializer(comment)

    return Response(serializer.data)

@api_view(['GET'])
def get_author_courses(request, user_id):
    user = User.objects.get(pk=user_id)
    courses = user.courses.filter(status=Course.PUBLISHED)

    user_serializer = UserSerializer(user, many=False)
    courses_serializer = CourseListSerializer(courses, many=True)

    return Response({
        'courses': courses_serializer.data,
        'created_by': user_serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz_answers(request, course_slug, lesson_slug):
    user_answers = request.data
    lesson = Lesson.objects.get(slug=lesson_slug)

    score = 0
    total_questions = 0
    results = []

    for answer_data in user_answers:
        total_questions += 1
        question_id = answer_data.get('question_id')
        selected_answer = answer_data.get('selected_answer')

        try:
            question = Quiz.objects.get(id=question_id, lesson=lesson)
            correct = False
            if question.answer == selected_answer:
                score += 1
                correct = True

            results.append({
                'question_id': question.id,
                'selected_answer': selected_answer,
                'correct': correct,
                'correct_answer': question.answer
            })
        except Quiz.DoesNotExist:
            # Handle case where question_id is invalid or doesn't belong to the lesson
            results.append({
                'question_id': question_id,
                'selected_answer': selected_answer,
                'correct': False,
                'correct_answer': None, # Or some indicator that the question was not found
                'error': 'Question not found or does not belong to this lesson.'
            })

    return Response({
        'score': score,
        'total_questions': total_questions,
        'results': results
    })