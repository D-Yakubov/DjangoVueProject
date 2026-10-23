# LMS Platform — Django & Vue.js

A full-stack Learning Management System (LMS) built with a Django REST Framework backend (`lms_project`) and a Vue 3 + Vuex + Bulma frontend (`lms_vue_project`).

## Features
- **Authentication & Authorization**: Token-based authentication via Djoser (`SignUp`, `LogIn`, `LogOut`, and protected `Dashboard` routes).
- **Course Management**: Instructors can create courses (`draft`, `in_review`, `published`) with dynamic lessons and category assignments.
- **Course Catalog & Filtering**: Browse published courses on the landing page, filter by category, or view courses by instructor.
- **Interactive Lesson Types**:
  - **Articles** with a student discussion/commenting system
  - **Video lessons** with embedded YouTube playback
  - **Quizzes** with instant answer verification
- **Progress Tracking**: Tracks started and completed lessons per student (`Activity`).

## Project Structure

```text
DjangoVueProject/
├── .gitignore
├── README.md
├── lms_project/                      # Django Backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── activity/                     # Student progress tracking app
│   ├── course/                       # Courses, categories, lessons, quizzes, comments app
│   └── lms_project/                  # Project settings & root URL configuration
└── lms_vue_project/                  # Vue 3 Frontend
    ├── package.json
    ├── public/
    └── src/
        ├── App.vue
        ├── main.js
        ├── components/
        │   ├── AddComment.vue
        │   ├── AppFooter.vue
        │   ├── AppNavbar.vue
        │   ├── CourseComment.vue
        │   ├── CourseItem.vue
        │   ├── LessonQuiz.vue
        │   └── LessonVideo.vue
        ├── router/
        │   └── index.js
        ├── store/
        │   └── index.js
        └── views/
            ├── AboutView.vue
            ├── AuthorCoursesView.vue
            ├── CourseDetailView.vue
            ├── CourseListView.vue
            ├── HomeView.vue
            ├── LoginView.vue
            ├── SignupView.vue
            └── dashboard/
                ├── CreateCourseView.vue
                └── MyAccountView.vue
```

## Setup & Installation

### 1. Backend (`lms_project`)

```bash
cd lms_project
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

### 2. Frontend (`lms_vue_project`)

```bash
cd lms_vue_project
npm install
npm run serve
```
