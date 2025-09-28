from django.core.management.base import BaseCommand
from courses.models import Level, Lesson, Exercise
import json

class Command(BaseCommand):
    help = 'Load German language quizzes from A1 to B2 levels'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to load German quizzes...'))
        
        # Define quizzes data
        quizzes_data = {
            'A1': [
                {
                    'title': 'Basic Greetings and Phrases',
                    'questions': [
                        {
                            'question': 'How do you say "Hello" in German?',
                            'type': 'mcq',
                            'options': ["Guten Morgen", "Hallo", "Tschüss"],
                            'answer': 'Hallo',
                            'explanation': 'The German word for "Hello" is "Hallo".'
                        },
                        {
                            'question': 'Translate to German: "Thank you"',
                            'type': 'mcq',
                            'options': ["Danke", "Bitte", "Entschuldigung"],
                            'answer': 'Danke',
                            'explanation': 'The German word for "Thank you" is "Danke".'
                        },
                        {
                            'question': 'Complete the sentence: Ich ___ Student.',
                            'type': 'mcq',
                            'options': ["bin", "bist", "seid"],
                            'answer': 'bin',
                            'explanation': 'The correct form is "Ich bin Student" which means "I am a student".'
                        }
                    ]
                }
            ],
            'A2': [
                {
                    'title': 'Basic Grammar and Vocabulary',
                    'questions': [
                        {
                            'question': 'Which sentence is correct?',
                            'type': 'mcq',
                            'options': [
                                "Ich habe ein Buch gelesen.",
                                "Ich habe Buch gelesen.",
                                "Ich gelesen habe ein Buch."
                            ],
                            'answer': 'Ich habe ein Buch gelesen.',
                            'explanation': 'The correct sentence structure in German is subject-verb-object with the correct article.'
                        },
                        {
                            'question': 'What does "die Stadt" mean?',
                            'type': 'mcq',
                            'options': ["The country", "The city", "The house"],
                            'answer': 'The city',
                            'explanation': '"Die Stadt" translates to "The city" in English.'
                        },
                        {
                            'question': 'Choose the correct verb form: Er ___ gern Fußball.',
                            'type': 'mcq',
                            'options': ["spielt", "spielen", "spielst"],
                            'answer': 'spielt',
                            'explanation': 'The correct conjugation for "er/sie/es" is "spielt".'
                        }
                    ]
                }
            ],
            'B1': [
                {
                    'title': 'Intermediate Grammar and Usage',
                    'questions': [
                        {
                            'question': 'Choose the correct translation: "I would like to order a coffee."',
                            'type': 'mcq',
                            'options': [
                                "Ich möchte einen Kaffee bestellen.",
                                "Ich will Kaffee trinken.",
                                "Ich kann Kaffee kaufen."
                            ],
                            'answer': 'Ich möchte einen Kaffee bestellen.',
                            'explanation': 'The polite form to order something is "Ich möchte..." which means "I would like..."'
                        },
                        {
                            'question': 'What is the correct passive form? "Die Schüler lesen das Buch."',
                            'type': 'mcq',
                            'options': [
                                "Das Buch wird von den Schülern gelesen.",
                                "Das Buch lesen die Schüler.",
                                "Das Buch ist die Schüler gelesen."
                            ],
                            'answer': 'Das Buch wird von den Schülern gelesen.',
                            'explanation': 'The passive voice in German is formed with "werden" + past participle.'
                        },
                        {
                            'question': 'Translate to English: "Es gibt viele Möglichkeiten, Deutsch zu lernen."',
                            'type': 'mcq',
                            'options': [
                                "There is many options to learn German.",
                                "There are many ways to learn German.",
                                "There is some way to learn German."
                            ],
                            'answer': 'There are many ways to learn German.',
                            'explanation': 'The phrase means "There are many ways to learn German."'
                        }
                    ]
                }
            ],
            'B2': [
                {
                    'title': 'Advanced Grammar and Complex Sentences',
                    'questions': [
                        {
                            'question': 'Choose the correct Konjunktiv II form: "Wenn ich Zeit ___, würde ich nach Berlin reisen."',
                            'type': 'mcq',
                            'options': ["habe", "hätte", "hattest"],
                            'answer': 'hätte',
                            'explanation': 'The Konjunktiv II form of "haben" is "hätte" for the first and third person singular.'
                        },
                        {
                            'question': 'What does "obwohl" mean?',
                            'type': 'mcq',
                            'options': ["because", "although", "however"],
                            'answer': 'although',
                            'explanation': '"Obwohl" means "although" in English and introduces a concessive clause.'
                        },
                        {
                            'question': 'Choose the correct preposition: "Ich warte ___ den Bus."',
                            'type': 'mcq',
                            'options': ["auf", "für", "an"],
                            'answer': 'auf',
                            'explanation': 'The correct preposition with "warten" is "auf" (to wait for).'
                        }
                    ]
                }
            ]
        }
        
        # Process each level
        for level_name, quizzes in quizzes_data.items():
            try:
                level = Level.objects.get(name=level_name)
                self.stdout.write(self.style.SUCCESS(f'Processing level: {level_name}'))
                
                for quiz in quizzes:
                    # Create or get the quiz lesson
                    lesson, created = Lesson.objects.get_or_create(
                        title=f"{level_name} Quiz: {quiz['title']}",
                        level=level,
                        defaults={
                            'slug': f"{level_name.lower()}-quiz-{quiz['title'].lower().replace(' ', '-')}",
                            'content': f"Interactive quiz for {level_name} level: {quiz['title']}",
                            'order': 99  # Place quizzes at the end
                        }
                    )
                    
                    # Add questions to the quiz
                    for i, question_data in enumerate(quiz['questions']):
                        Exercise.objects.update_or_create(
                            lesson=lesson,
                            question=question_data['question'],
                            defaults={
                                'type': question_data['type'],
                                'options': json.dumps(question_data['options']),
                                'answer': question_data['answer'],
                                'explanation': question_data.get('explanation', ''),
                                'order': i + 1
                            }
                        )
                    
                    self.stdout.write(self.style.SUCCESS(f'  - Added quiz: {quiz["title"]}'))
                    
            except Level.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Level {level_name} not found. Skipping...'))
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded all German quizzes!'))
