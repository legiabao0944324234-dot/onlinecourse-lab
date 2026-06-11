from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Home / course list
    path('', views.CourseListView.as_view(), name='index'),

    # Course detail
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),

    # Enrollment
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),

    # Submit exam answers  ← Task 6
    path('course/<int:course_id>/submit/', views.submit, name='submit'),

    # Show exam result     ← Task 6
    path(
        'course/<int:course_id>/submission/<int:submission_id>/result/',
        views.show_exam_result,
        name='show_exam_result',
    ),
]
