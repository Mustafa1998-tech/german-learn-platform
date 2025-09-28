from django.core.management.base import BaseCommand
from courses.models import Level, Lesson, Exercise
import json

class Command(BaseCommand):
    help = 'Load German language courses from A1 to C2 levels'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to load German courses...'))
        
        # Define levels data
        levels_data = [
            {'name': 'A1', 'description': 'Beginner'},
            {'name': 'A2', 'description': 'Elementary'},
            {'name': 'B1', 'description': 'Intermediate'},
            {'name': 'B2', 'description': 'Upper Intermediate'},
            {'name': 'C1', 'description': 'Advanced'},
            {'name': 'C2', 'description': 'Mastery'},
        ]
        
        # Define lessons data with YouTube URLs
        lessons_data = {
            'A1': [
                {
                    'title': 'Greetings and Self-Introduction',
                    'content': 'Hallo! Ich heiße [Name]. Ich komme aus [Land].',
                    'translation': 'مرحباً! اسمي [الاسم]. أنا من [البلد].',
                    'vocab': 'Hallo=مرحباً;Ich heiße=اسمي;Ich komme aus=أنا من',
                    'youtube_url': 'https://www.youtube.com/watch?v=J1i5rDRY2tE',
                    'exercises': [
                        {
                            'type': 'fill',
                            'question': 'Complete: ___! Ich heiße Mustafa.',
                            'answer': 'Hallo',
                            'explanation': 'Hallo means Hello in German.'
                        }
                    ]
                },
                {
                    'title': 'Numbers 1-20',
                    'content': '1 - eins\n2 - zwei\n3 - drei\n...\n20 - zwanzig',
                    'youtube_url': 'https://www.youtube.com/watch?v=4Zp4VvXIBiM',
                    'exercises': [
                        {
                            'type': 'mcq',
                            'question': 'What is the German word for 3?',
                            'options': '["eins", "zwei", "drei", "vier"]',
                            'answer': 'drei'
                        }
                    ]
                }
            ],
            'A2': [
                {
                    'title': 'Family',
                    'content': 'Das ist meine Mutter. Sie heißt Aisha.\nMein Vater ist Lehrer.',
                    'translation': 'هذه أمي. اسمها عائشة.\nوالدي معلم.',
                    'vocab': 'Mutter=أم;Vater=أب;Lehrer=معلّم',
                    'youtube_url': 'https://www.youtube.com/watch?v=Zl0iq2HhR6M'
                },
                {
                    'title': 'Daily Activities',
                    'content': 'Ich gehe zur Schule.\nEr arbeitet im Büro.\nWir essen um 19 Uhr.',
                    'youtube_url': 'https://www.youtube.com/watch?v=w1VvI3fSxg0'
                }
            ],
            'B1': [
                {
                    'title': 'Past Tense',
                    'content': 'Ich ging nach Hause.\nEr hat das Buch gelesen.\nWir haben gegessen.',
                    'youtube_url': 'https://www.youtube.com/watch?v=7_E9jHQpFMs'
                },
                {
                    'title': 'Passive Voice',
                    'content': 'Das Buch wird von mir gelesen.\nDas Buch wurde gelesen.\nDas Buch ist gelesen worden.',
                    'youtube_url': 'https://www.youtube.com/watch?v=H2qKk0Jq9Hg'
                }
            ],
            'B2': [
                {
                    'title': 'Expressing Opinions',
                    'content': 'Meiner Meinung nach ist Deutsch eine schöne Sprache.\nIch finde, dass das Wetter heute schön ist.',
                    'youtube_url': 'https://www.youtube.com/watch?v=VQf0bDgHeTQ'
                },
                {
                    'title': 'Conditional Sentences',
                    'content': 'Wenn ich Zeit hätte, würde ich nach Deutschland reisen.\nHätte ich mehr Geld, würde ich ein Auto kaufen.',
                    'youtube_url': 'https://www.youtube.com/watch?v=8NlZ2-w1n3Y'
                }
            ],
            'C1': [
                {
                    'title': 'Academic Language',
                    'content': 'Die Auswirkungen der Globalisierung auf die Wirtschaft sind vielfältig.\nForschungsergebnisse zeigen, dass ...',
                    'youtube_url': 'https://www.youtube.com/watch?v=4iR-pJXh2Ak'
                },
                {
                    'title': 'Expressing Assumptions',
                    'content': 'Es könnte sein, dass das Projekt erfolgreich wird.\nMan nimmt an, dass die Zahlen steigen werden.',
                    'youtube_url': 'https://www.youtube.com/watch?v=GJ6rEfgQk1o'
                }
            ],
            'C2': [
                {
                    'title': 'Formal Writing',
                    'content': 'Sehr geehrte Damen und Herren,\n\nIch möchte mich für die Position als [Position] bewerben.\n\nMit freundlichen Grüßen,\n[Ihr Name]',
                    'youtube_url': 'https://www.youtube.com/watch?v=Z4T6m7x9WfU'
                },
                {
                    'title': 'Literary Texts',
                    'content': '„Der Zauberberg" von Thomas Mann ist ein komplexer Roman, der sich mit philosophischen Themen auseinandersetzt.',
                    'youtube_url': 'https://www.youtube.com/watch?v=Q3zJvR9X9oM'
                }
            ]
        }
        
        # Create or update levels
        for i, level_data in enumerate(levels_data):
            level, created = Level.objects.update_or_create(
                name=level_data['name'],
                defaults={
                    'slug': level_data['name'].lower(),
                    'description': level_data['description'],
                    'order': i + 1
                }
            )
            self.stdout.write(self.style.SUCCESS(f'Processed level: {level.name}'))
            
            # Create or update lessons for this level
            for j, lesson_data in enumerate(lessons_data.get(level.name, [])):
                lesson, created = Lesson.objects.update_or_create(
                    title=lesson_data['title'],
                    level=level,
                    defaults={
                        'slug': f"{level.name.lower()}-{lesson_data['title'].lower().replace(' ', '-')}",
                        'content': lesson_data['content'],
                        'translation': lesson_data.get('translation', ''),
                        'vocab': lesson_data.get('vocab', ''),
                        'youtube_url': lesson_data.get('youtube_url', ''),
                        'order': j + 1
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'  - Added lesson: {lesson.title}'))
                
                # Add exercises if any
                for k, exercise_data in enumerate(lesson_data.get('exercises', [])):
                    exercise, created = Exercise.objects.update_or_create(
                        lesson=lesson,
                        question=exercise_data['question'],
                        defaults={
                            'type': exercise_data['type'],
                            'options': exercise_data.get('options', ''),
                            'answer': exercise_data['answer'],
                            'explanation': exercise_data.get('explanation', ''),
                            'order': k + 1
                        }
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded all German courses!'))
