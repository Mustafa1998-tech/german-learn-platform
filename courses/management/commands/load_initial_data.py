from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
import os
from courses.models import Level, Lesson, Exercise
import json

class Command(BaseCommand):
    help = 'Load initial data for German Learning Platform'

    def handle(self, *args, **options):
        self.stdout.write('Loading initial data...')
        
        # Create levels
        levels_data = [
            {'name': 'A1', 'description': 'المستوى المبتدئ - يمكن فهم واستخدام التعابير اليومية والعبارات الأساسية'},
            {'name': 'A2', 'description': 'المستوى الأساسي - يمكن فهم الجمل والتعابير المتعلقة بمجالات ذات صلة مباشرة'},
            {'name': 'B1', 'description': 'المستوى المتوسط - يمكن التعامل مع معظم المواقف التي قد تنشأ أثناء السفر'},
            {'name': 'B2', 'description': 'المستوى فوق المتوسط - يمكن التفاعل بطلاقة وعفوية مع الناطقين الأصليين'},
            {'name': 'C1', 'description': 'المستوى المتقدم - يمكن التعبير عن الأفكار المعقدة بطلاقة وتلقائية'},
            {'name': 'C2', 'description': 'الكفاءة - يمكن فهم كل ما يسمع أو يقرأ بسهولة'}
        ]
        
        levels = {}
        for level_data in levels_data:
            level, created = Level.objects.get_or_create(
                name=level_data['name'],
                defaults={'description': level_data['description']}
            )
            levels[level.name] = level
            self.stdout.write(f"{'Created' if created else 'Updated'} level: {level.name}")
        
        # A1 Level Lessons
        a1_lessons = [
            {
                'title': 'التحية والتعريف بالنفس',
                'content': 'في هذا الدرس ستتعلم كيفية التحية والتعريف بنفسك بالألمانية.',
                'youtube_url': 'https://www.youtube.com/embed/GxcqTvwYL5o',
                'order': 1,
                'vocab': 'Hallo;Guten Tag;Guten Morgen;Guten Abend;Gute Nacht;Tschüss;Auf Wiedersehen;Wie geht es dir?;Mir geht es gut;Danke;Und dir?',
                'exercises': [
                    {
                        'type': 'mcq',
                        'question': 'ما هي التحية المناسبة في الصباح؟',
                        'options': '["Guten Tag", "Guten Morgen", "Gute Nacht"]',
                        'answer': 'Guten Morgen',
                        'explanation': 'Guten Morgen تعني صباح الخير وتستخدم للتحية في الصباح.'
                    },
                    {
                        'type': 'fill',
                        'question': 'كيف تسأل شخصاً كيف حاله بالألمانية؟',
                        'answer': 'Wie geht es dir?',
                        'explanation': 'Wie geht es dir? تعني كيف حالك؟ بالألمانية.'
                    }
                ]
            },
            {
                'title': 'الأرقام من 1 إلى 20',
                'content': 'تعلم كيفية العد من 1 إلى 20 بالألمانية.',
                'youtube_url': 'https://www.youtube.com/embed/5aP9DlWDZWg',
                'order': 2,
                'vocab': 'null;eins;zwei;drei;vier;fünf;sechs;sieben;acht;neun;zehn;elf;zwölf;dreizehn;vierzehn;fünfzehn;sechzehn;siebzehn;achtzehn;neunzehn;zwanzig',
                'exercises': [
                    {
                        'type': 'mcq',
                        'question': 'ما هو الرقم 15 بالألمانية؟',
                        'options': '["fünfzehn", "fünf", "fünfzig"]',
                        'answer': 'fünfzehn',
                        'explanation': 'fünfzehn تعني 15، بينما fünf تعني 5 و fünfzig تعني 50.'
                    },
                    {
                        'type': 'fill',
                        'question': 'اكتب الرقم 12 بالألمانية:',
                        'answer': 'zwölf',
                        'explanation': 'zwölf هو الرقم 12 بالألمانية.'
                    }
                ]
            },
            # يمكن إضافة المزيد من الدروس هنا
        ]

        # Add A1 lessons
        for lesson_data in a1_lessons:
            lesson, created = Lesson.objects.get_or_create(
                title=lesson_data['title'],
                level=levels['A1'],
                defaults={
                    'content': lesson_data['content'],
                    'youtube_url': lesson_data['youtube_url'],
                    'order': lesson_data['order'],
                    'vocab': lesson_data['vocab']
                }
            )
            
            # Add exercises for the lesson
            for ex_data in lesson_data.get('exercises', []):
                Exercise.objects.get_or_create(
                    lesson=lesson,
                    type=ex_data['type'],
                    question=ex_data['question'],
                    defaults={
                        'options': ex_data.get('options', ''),
                        'answer': ex_data['answer'],
                        'explanation': ex_data.get('explanation', '')
                    }
                )
            
            self.stdout.write(f"{'Created' if created else 'Updated'} lesson: {lesson.title}")
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data!'))
