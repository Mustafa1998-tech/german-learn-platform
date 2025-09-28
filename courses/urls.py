from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('level/<slug:level_slug>/', views.LevelDetailView.as_view(), name='level_detail'),
    path('lesson/<slug:lesson_slug>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('api/quiz/<slug:lesson_slug>/', views.process_quiz, name='process_quiz'),
    path('api/generate-audio/<int:lesson_id>/', views.generate_audio, name='generate_audio'),
]
