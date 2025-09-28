from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Level, Lesson, Exercise, Result
import json

class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['levels'] = Level.objects.all().order_by('order')
        return context

class LevelDetailView(DetailView):
    model = Level
    template_name = 'level.html'
    context_object_name = 'level'
    slug_url_kwarg = 'level_slug'
    
    def get_queryset(self):
        return Level.objects.prefetch_related('lessons').all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = self.object.lessons.all().order_by('order')
        return context

class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lesson.html'
    context_object_name = 'lesson'
    slug_url_kwarg = 'lesson_slug'
    
    def get_queryset(self):
        return Lesson.objects.select_related('level')\
                           .prefetch_related('exercises')\
                           .all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        
        # Get next and previous lessons
        lessons_in_level = list(Lesson.objects.filter(level=lesson.level)
                                   .order_by('order'))
        current_index = lessons_in_level.index(lesson)
        
        context['next_lesson'] = lessons_in_level[current_index + 1] if current_index < len(lessons_in_level) - 1 else None
        context['prev_lesson'] = lessons_in_level[current_index - 1] if current_index > 0 else None
        
        # Get user's previous result if exists
        if self.request.user.is_authenticated:
            try:
                context['user_result'] = Result.objects.get(
                    user=self.request.user, 
                    lesson=lesson
                )
            except Result.DoesNotExist:
                context['user_result'] = None
        
        return context

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@csrf_exempt
def process_quiz(request, lesson_slug):
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        data = json.loads(request.body)
        answers = data.get('answers', {})
        
        correct = 0
        total = lesson.exercises.count()
        results = {}
        
        for exercise in lesson.exercises.all():
            user_answer = answers.get(str(exercise.id), '').strip()
            is_correct = False
            
            if exercise.type == 'mcq':
                is_correct = user_answer == exercise.answer
            elif exercise.type == 'tf':
                is_correct = user_answer.lower() == exercise.answer.lower()
            elif exercise.type == 'fill':
                is_correct = user_answer.lower() == exercise.answer.lower()
            
            if is_correct:
                correct += 1
            
            results[str(exercise.id)] = {
                'is_correct': is_correct,
                'correct_answer': exercise.answer,
                'explanation': exercise.explanation or ''
            }
        
        score = round((correct / total) * 100) if total > 0 else 0
        
        # Save result if user is authenticated
        if request.user.is_authenticated:
            Result.objects.update_or_create(
                user=request.user,
                lesson=lesson,
                defaults={
                    'score': score,
                    'completed': True,
                    'answers': answers
                }
            )
        
        return JsonResponse({
            'success': True,
            'score': score,
            'results': results
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def generate_audio(request, lesson_id):
    # This would be implemented to generate audio using gTTS
    # For now, it's a placeholder
    return JsonResponse({'status': 'success'})
