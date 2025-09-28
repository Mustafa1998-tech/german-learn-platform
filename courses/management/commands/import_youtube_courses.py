import os
import json
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from courses.models import Level, Lesson, Exercise

class Command(BaseCommand):
    help = 'Import initial data for German learning platform (Levels, Lessons, Exercises)'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to import initial data...'))
        
        # Define the initial data
        levels_data = [
            {
                'name': 'A1',
                'slug': 'a1',
                'description': 'Anfänger - Grundkenntnisse',
                'order': 1
            },
            {
                'name': 'A2',
                'slug': 'a2',
                'description': 'Grundlegende Kenntnisse',
                'order': 2
            },
            {
                'name': 'B1',
                'slug': 'b1',
                'description': 'Fortgeschrittene Sprachverwendung',
                'order': 3
            },
            {
                'name': 'B2',
                'slug': 'b2',
                'description': 'Selbstständige Sprachverwendung',
                'order': 4
            },
            {
                'name': 'C1',
                'slug': 'c1',
                'description': 'Fachkundige Sprachkenntnisse',
                'order': 5
            },
            {
                'name': 'C2',
                'slug': 'c2',
                'description': 'Annähernd muttersprachliche Kenntnisse',
                'order': 6
            },
        ]
        
        # Sample lessons data (5 per level)
        lessons_data = {
            'A1': [
                {
                    'title': 'Begrüßungen und Vorstellungen',
                    'slug': 'a1-begruessungen-und-vorstellungen',
                    'youtube_url': 'https://www.youtube.com/watch?v=6_b7RDuawgo',
                    'content': """
                    <p><strong>Hallo!</strong> Mein Name ist Anna. Ich komme aus Deutschland. Ich lerne Deutsch.</p>
                    <p><strong>Guten Tag!</strong> Ich heiße Max. Ich bin 25 Jahre alt. Ich wohne in Berlin.</p>
                    <p>Wie heißt du? Woher kommst du? Wie alt bist du?</p>
                    <p>Das ist mein Freund, Tom. Er kommt aus Österreich.</p>
                    <p>Freut mich, dich kennenzulernen!</p>
                    """,
                    'translation': """
                    <p><strong>مرحباً!</strong> اسمي آنا. أنا من ألمانيا. أتعلم اللغة الألمانية.</p>
                    <p><strong>مرحباً!</strong> اسمي ماكس. عمري 25 سنة. أسكن في برلين.</p>
                    <p>ما اسمك؟ من أين أنت؟ كم عمرك؟</p>
                    <p>هذا صديقي توم. هو من النمسا.</p>
                    <p>تشرفت بمعرفتك!</p>
                    """,
                    'vocab': 'Hallo;Guten Tag;Ich heiße;Mein Name ist;kommen aus;wohnen;lernen;Freund;Freut mich;kennenlernen',
                    'exercises': [
                        {
                            'type': 'mcq',
                            'question': 'Was bedeutet "Hallo"?',
                            'options': ['Goodbye', 'Hello', 'Thank you', 'Please'],
                            'answer': 1,
                            'explanation': '"Hallo" bedeutet "Hello" auf Englisch.'
                        },
                        {
                            'type': 'tf',
                            'question': '"Ich komme aus Deutschland" bedeutet "I am from Germany".',
                            'answer': True,
                            'explanation': 'Richtig! "Ich komme aus..." bedeutet "I am from..."'
                        },
                        {
                            'type': 'fill',
                            'question': '_____ Name ist Anna. (My)',
                            'answer': 'Mein',
                            'explanation': '"Mein Name ist..." bedeutet "My name is..."'
                        },
                        {
                            'type': 'mcq',
                            'question': 'Was sagt man, wenn man jemanden kennenlernt?',
                            'options': ['Tschüss', 'Guten Morgen', 'Freut mich', 'Auf Wiedersehen'],
                            'answer': 2,
                            'explanation': '"Freut mich" sagt man, wenn man jemanden kennenlernt.'
                        }
                    ]
                },
                {
                    'title': 'Zahlen von 1-100',
                    'slug': 'a1-zahlen-1-100',
                    'youtube_url': 'https://www.youtube.com/watch?v=4wRBlRJ8XV4',
                    'content': """
                    <p>Die Zahlen von 1-10:</p>
                    <p>1 - eins, 2 - zwei, 3 - drei, 4 - vier, 5 - fünf, 6 - sechs, 7 - sieben, 8 - acht, 9 - neun, 10 - zehn</p>
                    <p>11 - elf, 12 - zwölf, 13 - dreizehn, ..., 20 - zwanzig</p>
                    <p>21 - einundzwanzig, 22 - zweiundzwanzig, ..., 30 - dreißig</p>
                    <p>31 - einunddreißig, 32 - zweiunddreißig, ..., 100 - hundert</p>
                    """,
                    'vocab': 'eins;zwei;drei;vier;fünf;sechs;sieben;acht;neun;zehn;elf;zwölf;zwanzig;dreißig;vierzig;fünfzig;sechzig;siebzig;achtzig;neunzig;hundert',
                    'exercises': [
                        {
                            'type': 'mcq',
                            'question': 'Wie sagt man "25" auf Deutsch?',
                            'options': ['fünfundzwanzig', 'zwanzigfünf', 'fünfundzwanzig', 'fünfundzwanzig'],
                            'answer': 0,
                            'explanation': '25 heißt "fünfundzwanzig" auf Deutsch.'
                        },
                        {
                            'type': 'fill',
                            'question': 'Schreiben Sie die Zahl: 42',
                            'answer': 'zweiundvierzig',
                            'explanation': '42 heißt "zweiundvierzig" auf Deutsch.'
                        }
                    ]
                },
                {
                    'title': 'Im Restaurant',
                    'slug': 'a1-im-restaurant',
                    'youtube_url': 'https://www.youtube.com/watch?v=7iXFSJBMr28',
                    'content': """
                    <p>Guten Abend! Haben Sie einen Tisch frei?</p>
                    <p>Für wie viele Personen? - Für zwei Personen, bitte.</p>
                    <p>Die Speisekarte, bitte. - Hier, bitte schön.</p>
                    <p>Ich hätte gerne die Gemüsesuppe und ein Mineralwasser.</p>
                    <p>Möchten Sie noch etwas? - Nein, danke. Das war alles.</p>
                    <p>Zahlen, bitte! - Das macht 15,50 Euro, bitte.</p>
                    """,
                    'vocab': 'Restaurant;Tisch;frei;Personen;Speisekarte;bestellen;trinken;essen;bezahlen;Trinkgeld',
                    'exercises': [
                        {
                            'type': 'mcq',
                            'question': 'Was sagt man, wenn man die Rechnung haben möchte?',
                            'options': ['Zahlen, bitte!', 'Guten Appetit!', 'Auf Wiedersehen!', 'Danke schön!'],
                            'answer': 0,
                            'explanation': '"Zahlen, bitte!" sagt man, wenn man die Rechnung haben möchte.'
                        }
                    ]
                },
                {
                    'title': 'Tagesablauf',
                    'slug': 'a1-tagesablauf',
                    'youtube_url': 'https://www.youtube.com/watch?v=3a7nslsx7WU',
                    'content': """
                    <p>Mein Tagesablauf:</p>
                    <p>Um 7 Uhr stehe ich auf.</p>
                    <p>Um halb acht frühstücke ich.</p>
                    <p>Um 8 Uhr fahre ich zur Arbeit.</p>
                    <p>Von 9 bis 17 Uhr arbeite ich.</p>
                    <p>Um 18 Uhr koche ich Abendessen.</p>
                    <p>Um 23 Uhr gehe ich schlafen.</p>
                    """,
                    'vocab': 'aufstehen;frühstücken;arbeiten;Mittagspause;nach Hause gehen;Abendessen;kochen;fernsehen;schlafen gehen;Tagesablauf',
                    'exercises': []
                },
                {
                    'title': 'Einkaufen',
                    'slug': 'a1-einkaufen',
                    'youtube_url': 'https://www.youtube.com/watch?v=3a7nslsx7WU',
                    'content': """
                    <p>Wo ist der Supermarkt? - Dort drüben.</p>
                    <p>Was kostet das? - Das kostet 2,99 Euro.</p>
                    <p>Ich hätte gerne ein Kilo Äpfel, bitte.</p>
                    <p>Haben Sie Milch? - Ja, im Kühlregal hinten links.</p>
                    <p>Zahlen Sie mit Karte oder bar? - Mit Karte, bitte.</p>
                    """,
                    'vocab': 'Supermarkt;Markt;einkaufen;verkaufen;Preis;teuer;billig;Kasse;Einkaufswagen;Einkaufstasche',
                    'exercises': []
                }
            ],
            'A2': [
                {
                    'title': 'Perfekt: Vergangenheit',
                    'slug': 'a2-perfekt-vergangenheit',
                    'youtube_url': 'https://www.youtube.com/watch?v=Y5t4ogntf6k',
                    'content': """
                    <p>Das Perfekt ist eine Zeitform der Vergangenheit.</p>
                    <p>Bildung: haben/sein + Partizip II</p>
                    <p>Beispiele:</p>
                    <p>Ich habe Deutsch gelernt. (lernen - gelernt)</p>
                    <p>Sie ist nach Hause gegangen. (gehen - gegangen)</p>
                    <p>Wir haben einen Film gesehen. (sehen - gesehen)</p>
                    """,
                    'vocab': 'haben;sein;Partizip;Vergangenheit;gestern;letzte Woche;vor einem Jahr;schon;noch nicht;gerade',
                    'exercises': []
                },
                {
                    'title': 'Dativ: Wem?',
                    'slug': 'a2-dativ',
                    'youtube_url': 'https://www.youtube.com/watch?v=Y5t4ogntf6k',
                    'content': """
                    <p>Der Dativ antwortet auf die Frage "Wem?".</p>
                    <p>Beispiele:</p>
                    <p>Ich gebe dem Mann ein Buch. (Wem gebe ich ein Buch? - Dem Mann)</p>
                    <p>Ich helfe der Frau. (Wem helfe ich? - Der Frau)</p>
                    <p>Ich antworte dem Kind. (Wem antworte ich? - Dem Kind)</p>
                    """,
                    'vocab': 'geben;helfen;antworten;gehören;danken;gefallen;schmecken;passen;glauben;folgen',
                    'exercises': []
                }
            ],
            'B1': [
                {
                    'title': 'Konjunktiv II',
                    'slug': 'b1-konjunktiv-ii',
                    'youtube_url': 'https://www.youtube.com/watch?v=Y5t4ogntf6k',
                    'content': """
                    <p>Der Konjunktiv II wird für irreale Wünsche, Träume und höfliche Bitten verwendet.</p>
                    <p>Beispiele:</p>
                    <p>Ich hätte gerne einen Kaffee. (Höfliche Bitte)</p>
                    <p>Ich wäre gerne reich. (Irrealer Wunsch)</p>
                    <p>Wenn ich Zeit hätte, würde ich mehr lesen. (Irreale Bedingung)</p>
                    """,
                    'vocab': 'würde;hätte;wäre;könnte;müsste;sollte;wenn;als ob;wünschen;träumen',
                    'exercises': []
                }
            ],
            'B2': [
                {
                    'title': 'Passiv',
                    'slug': 'b2-passiv',
                    'youtube_url': 'https://www.youtube.com/watch?v=Y5t4ogntf6k',
                    'content': """
                    <p>Das Passiv wird verwendet, wenn das Subjekt nicht wichtig ist oder unbekannt ist.</p>
                    <p>Bildung: werden + Partizip II</p>
                    <p>Beispiele:</p>
                    <p>Das Buch wird (von mir) gelesen. (Präsens)</p>
                    <p>Das Buch wurde gelesen. (Präteritum)</p>
                    <p>Das Buch ist gelesen worden. (Perfekt)</p>
                    """,
                    'vocab': 'werden;worden;geworden;von;man;es gibt;scheinen;heißen;bleiben;gelten',
                    'exercises': []
                }
            ],
            'C1': [
                {
                    'title': 'Konjunktiv I',
                    'slug': 'c1-konjunktiv-i',
                    'youtube_url': 'https://www.youtube.com/watch?v=Y5t4ogntf6k',
                    'content': """
                    <p>Der Konjunktiv I wird hauptsächlich in der indirekten Rede verwendet.</p>
                    <p>Beispiele:</p>
                    <p>Er sagt, er habe keine Zeit. (Indirekte Rede)</p>
                    <p>Sie meint, sie komme später. (Indirekte Rede)</p>
                    <p>Man nehme 100g Mehl. (Aufforderungssatz in Rezepten)</p>
                    """,
                    'vocab': 'sagen;meinen;behaupten;behaupten;behaupten;behaupten;behaupten;behaupten;behaupten;behaupten',
                    'exercises': []
                }
            ],
            'C2': [
                {
                    'title': 'Nominalstil',
                    'slug': 'c2-nominalstil',
                    'youtube_url': 'https://www.youtube.com/watch?v=Y5t4ogntf6k',
                    'content': """
                    <p>Im Nominalstil werden Verben durch Nomen ersetzt.</p>
                    <p>Beispiele:</p>
                    <p>Wir bauen ein Haus. → Der Bau eines Hauses</p>
                    <p>Sie diskutieren über Politik. → Die Diskussion über Politik</p>
                    <p>Er forscht an der Universität. → Seine Forschung an der Universität</p>
                    """,
                    'vocab': 'Bau;Diskussion;Forschung;Entwicklung;Veränderung;Verbesserung;Verschlechterung;Zunahme;Abnahme;Auswirkung',
                    'exercises': []
                }
            ]
        }
        
        # Create levels
        for level_data in levels_data:
            level, created = Level.objects.update_or_create(
                name=level_data['name'],
                defaults={
                    'slug': level_data['slug'],
                    'description': level_data['description'],
                    'order': level_data['order']
                }
            )
            
            action = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{action} level: {level.name}'))
            
            # Add lessons for this level if they exist
            level_lessons = lessons_data.get(level.name, [])
            
            for lesson_index, lesson_data in enumerate(level_lessons, 1):
                lesson, created = Lesson.objects.update_or_create(
                    slug=lesson_data['slug'],
                    defaults={
                        'title': lesson_data['title'],
                        'level': level,
                        'content': lesson_data['content'].strip(),
                        'translation': lesson_data.get('translation', '').strip(),
                        'vocab': lesson_data.get('vocab', ''),
                        'youtube_url': lesson_data.get('youtube_url', ''),
                        'order': lesson_index
                    }
                )
                
                action = 'Created' if created else 'Updated'
                self.stdout.write(f'  {action} lesson: {lesson.title}')
                
                # Add exercises for this lesson
                exercises = lesson_data.get('exercises', [])
                
                for ex_index, exercise_data in enumerate(exercises, 1):
                    exercise, created = Exercise.objects.update_or_create(
                        lesson=lesson,
                        order=ex_index,
                        defaults={
                            'type': exercise_data['type'],
                            'question': exercise_data['question'],
                            'options': json.dumps(exercise_data.get('options', [])),
                            'answer': str(exercise_data['answer']),
                            'explanation': exercise_data.get('explanation', '')
                        }
                    )
                    
                    action = 'Created' if created else 'Updated'
                    self.stdout.write(f'    {action} exercise: {exercise.question[:50]}...')
        
        self.stdout.write(self.style.SUCCESS('Successfully imported all data!'))
