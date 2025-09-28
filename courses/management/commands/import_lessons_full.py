from django.core.management.base import BaseCommand
from courses.models import Level, Lesson, Exercise
import json

class Command(BaseCommand):
    help = 'Load complete German courses with lessons, videos, and quizzes from A1 to C2'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to import complete German courses...'))
        
        # Define complete course structure with YouTube videos
        courses_data = {
            'A1': [
                {
                    'title': 'Greetings and Self-Introduction',
                    'slug': 'a1-greetings-and-self-introduction',
                    'content': '''<div class="video-container">
                        <iframe width="560" height="315" src="https://www.youtube.com/embed/5MgBikgcWnY" frameborder="0" allowfullscreen></iframe>
                    </div>
                    <h2>Greetings and Self-Introduction</h2>
                    <p>Learn how to greet people and introduce yourself in German.</p>
                    <h3>Basic Greetings:</h3>
                    <ul>
                        <li>Hallo! - Hello!</li>
                        <li>Guten Morgen! - Good morning!</li>
                        <li>Guten Tag! - Good day!</li>
                        <li>Guten Abend! - Good evening!</li>
                        <li>Tschüss! - Bye!</li>
                    </ul>
                    <h3>Self-Introduction:</h3>
                    <ul>
                        <li>Ich heiße... - My name is...</li>
                        <li>Ich komme aus... - I am from...</li>
                        <li>Ich wohne in... - I live in...</li>
                        <li>Ich bin... Jahre alt. - I am ... years old.</li>
                    </ul>''',
                    'translation': '''<h2>التحية والتعريف بالنفس</h2>
                    <p>تعلم كيف تحيي الآخرين وتعرف بنفسك باللغة الألمانية.</p>
                    <h3>التحيات الأساسية:</h3>
                    <ul>
                        <li>مرحباً!</li>
                        <li>صباح الخير!</li>
                        <li>نهارك سعيد!</li>
                        <li>مساء الخير!</li>
                        <li>إلى اللقاء!</li>
                    </ul>
                    <h3>التعريف بالنفس:</h3>
                    <ul>
                        <li>اسمي...</li>
                        <li>أنا من...</li>
                        <li>أعيش في...</li>
                        <li>عمري... سنة.</li>
                    </ul>''',
                    'vocab': 'Hallo=مرحباً;Guten Morgen=صباح الخير;Guten Tag=نهارك سعيد;Guten Abend=مساء الخير;Tschüss=إلى اللقاء;Ich heiße=اسمي;Ich komme aus=أنا من;Ich wohne in=أعيش في;Jahre alt=سنوات من العمر',
                    'youtube_url': 'https://www.youtube.com/embed/5MgBikgcWnY',
                    'exercises': [
                        {
                            'type': 'mcq',
                            'question': 'What does "Hallo" mean in English?',
                            'options': '["Hello", "Goodbye", "Thank you"]',
                            'answer': 'Hello',
                            'explanation': 'The German word "Hallo" means "Hello" in English.'
                        },
                        {
                            'type': 'fill',
                            'question': 'Complete the greeting: ___ Morgen! (Good morning!)',
                            'answer': 'Guten',
                            'explanation': 'The correct phrase is "Guten Morgen!" which means "Good morning!"'
                        },
                        {
                            'type': 'mcq',
                            'question': 'How do you say "My name is" in German?',
                            'options': '["Ich bin", "Ich heiße", "Ich komme"]',
                            'answer': 'Ich heiße',
                            'explanation': 'The correct phrase is "Ich heiße" which means "My name is" or "I am called"'
                        }
                    ]
                },
                # Add more A1 lessons here...
            ],
            'A2': [
                {
                    'title': 'Family and Relationships',
                    'slug': 'a2-family-relationships',
                    'content': '''<div class="video-container">
                        <iframe width="560" height="315" src="https://www.youtube.com/embed/1d1aZqPTXUY" frameborder="0" allowfullscreen></iframe>
                    </div>
                    <h2>Family and Relationships</h2>
                    <p>Learn how to talk about your family and relationships in German.</p>
                    <h3>Family Members:</h3>
                    <ul>
                        <li>die Familie - family</li>
                        <li>die Mutter - mother</li>
                        <li>der Vater - father</li>
                        <li>die Eltern - parents</li>
                        <li>die Schwester - sister</li>
                        <li>der Bruder - brother</li>
                        <li>die Tochter - daughter</li>
                        <li>der Sohn - son</li>
                    </ul>''',
                    'youtube_url': 'https://www.youtube.com/embed/Zl0iq2HhR6M',
                    'exercises': [
                        {
                            'type': 'mcq',
                            'question': 'What does "die Mutter" mean in English?',
                            'options': '["Father", "Mother", "Sister"]',
                            'answer': 'Mother',
                            'explanation': 'The German word "die Mutter" means "mother" in English.'
                        }
                    ]
                }
                # Add more A2 lessons here...
            ],
            'B1': [
                {
                    'title': 'Daily Routine',
                    'slug': 'b1-daily-routine',
                    'content': '''<div class="video-container">
                        <iframe width="560" height="315" src="https://www.youtube.com/embed/C0DPdy98e4c" frameborder="0" allowfullscreen></iframe>
                    </div>
                    <h2>Daily Routine</h2>
                    <p>Learn how to talk about your daily activities in German.</p>
                    <h3>Common Daily Activities:</h3>
                    <ul>
                        <li>Aufstehen - to get up</li>
                        <li>Frühstücken - to have breakfast</li>
                        <li>Zur Arbeit gehen - to go to work</li>
                        <li>Zu Mittag essen - to have lunch</n                        <li>Nach Hause kommen - to come home</li>
                        <li>Abendessen - to have dinner</li>
                        <li>Schlafen gehen - to go to bed</li>
                    </ul>''',
                    'youtube_url': 'https://www.youtube.com/embed/1d1aZqPTXUY',
                    'exercises': [
                        {
                            'type': 'mcq',
                            'question': 'What does "Frühstücken" mean?',
                            'options': '["To have breakfast", "To have lunch", "To have dinner"]',
                            'answer': 'To have breakfast',
                            'explanation': 'The German word "Frühstücken" means "to have breakfast" in English.'
                        }
                    ]
                }
            ],
            'B2': [
                {
                    'title': 'German Culture and Traditions',
                    'slug': 'b2-german-culture',
                    'content': '''<div class="video-container">
                        <iframe width="560" height="315" src="https://www.youtube.com/embed/7JSI5C0B5eQ" frameborder="0" allowfullscreen></iframe>
                    </div>
                    <h2>German Culture and Traditions</h2>
                    <p>Explore German culture, traditions, and social norms.</p>
                    <h3>Important Cultural Aspects:</h3>
                    <ul>
                        <li>Pünktlichkeit (Punctuality) - Germans value being on time</li>
                        <li>Recycling and Environmental Awareness</li>
                        <li>German Cuisine and Beer Culture</li>
                        <li>Christmas Markets and Festivals</li>
                    </ul>''',
                    'youtube_url': 'https://www.youtube.com/embed/7JSI5C0B5eQ',
                    'exercises': [
                        {
                            'type': 'mcq',
                            'question': 'What is highly valued in German culture?',
                            'options': '["Being late", "Punctuality", "Improvisation"]',
                            'answer': 'Punctuality',
                            'explanation': 'Pünktlichkeit (punctuality) is highly valued in German culture.'
                        }
                    ]
                }
            ],
            'C1': [
                {
                    'title': 'Advanced German Grammar',
                    'slug': 'c1-advanced-grammar',
                    'content': '''<div class="video-container">
                        <iframe width="560" height="315" src="https://www.youtube.com/embed/7L4q1bP0uT4" frameborder="0" allowfullscreen></iframe>
                    </div>
                    <h2>Advanced German Grammar</h2>
                    <p>Master complex German grammar structures and usage.</p>
                    <h3>Topics Covered:</h3>
                    <ul>
                        <li>Subjunctive II (Konjunktiv II)</li>
                        <li>Passive Voice Advanced Usage</li>
                        <li>Nominalization</li>
                        <li>Complex Sentence Structures</li>
                    </ul>''',
                    'youtube_url': 'https://www.youtube.com/embed/7L4q1bP0uT4'
                }
            ],
            'C2': [
                {
                    'title': 'Business German',
                    'slug': 'c2-business-german',
                    'content': '''<div class="video-container">
                        <iframe width="560" height="315" src="https://www.youtube.com/embed/7pS5kP7qQJk" frameborder="0" allowfullscreen></iframe>
                    </div>
                    <h2>Business German</h2>
                    <p>Learn formal German for professional and business contexts.</p>
                    <h3>Key Business Topics:</h3>
                    <ul>
                        <li>Business Correspondence</li>
                        <li>Meetings and Negotiations</li>
                        <li>Business Etiquette</li>
                        <li>Professional Presentations</li>
                    </ul>''',
                    'youtube_url': 'https://www.youtube.com/embed/7pS5kP7qQJk'
                }
            ]
        }
        
        # Create or update levels and lessons
        for level_name, lessons in courses_data.items():
            # Create or get the level
            level, created = Level.objects.update_or_create(
                name=level_name,
                defaults={
                    'slug': level_name.lower(),
                    'description': f'German Language Level {level_name}'
                }
            )
            self.stdout.write(self.style.SUCCESS(f'Processed level: {level_name}'))
            
            # Create or update lessons for this level
            for lesson_data in lessons:
                lesson, created = Lesson.objects.update_or_create(
                    slug=lesson_data['slug'],
                    defaults={
                        'title': lesson_data['title'],
                        'content': lesson_data['content'],
                        'translation': lesson_data.get('translation', ''),
                        'vocab': lesson_data.get('vocab', ''),
                        'youtube_url': lesson_data.get('youtube_url', ''),
                        'level': level,
                        'order': 1  # You might want to adjust this
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'  - Added/Updated lesson: {lesson.title}'))
                
                # Add exercises if any
                for i, exercise_data in enumerate(lesson_data.get('exercises', [])):
                    Exercise.objects.update_or_create(
                        lesson=lesson,
                        question=exercise_data['question'],
                        defaults={
                            'type': exercise_data['type'],
                            'options': exercise_data.get('options', ''),
                            'answer': exercise_data['answer'],
                            'explanation': exercise_data.get('explanation', ''),
                            'order': i + 1
                        }
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully imported all German courses!'))
