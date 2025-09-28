import os
import json
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from courses.models import Level, Lesson, Exercise

class Command(BaseCommand):
    help = 'Import comprehensive German lessons from A1 to C2 levels'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to import German lessons...'))
        
        # Define the lessons data
        lessons_data = [
            # A1 Level Lessons
            {
                'level': 'A1',
                'title': 'التحية والتعريف بالنفس',
                'slug': 'a1-greetings',
                'youtube_url': 'https://www.youtube.com/watch?v=J1i5rDRY2tE',
                'content': 'Hallo! Ich heiße Mustafa. Ich komme aus Sudan.\nGuten Morgen! Wie geht es Ihnen?',
                'translation': 'مرحباً! أنا اسمي مصطفى. أنا من السودان.\nصباح الخير! كيف حالكم؟',
                'vocab': 'Hallo=مرحباً;Ich heiße=أنا اسمي;Wie geht es Ihnen=كيف حالكم',
                'order': 1
            },
            {
                'level': 'A1',
                'title': 'الأرقام من 1 إلى 20',
                'slug': 'a1-numbers',
                'youtube_url': 'https://www.youtube.com/watch?v=4Zp4VvXIBiM',
                'content': '1 eins\n2 zwei\n3 drei\n4 vier\n5 fünf\n6 sechs\n7 sieben\n8 acht\n9 neun\n10 zehn\n11 elf\n12 zwölf\n13 dreizehn\n14 vierzehn\n15 fünfzehn\n16 sechzehn\n17 siebzehn\n18 achtzehn\n19 neunzehn\n20 zwanzig',
                'translation': '1 واحد\n2 اثنان\n3 ثلاثة\n4 أربعة\n5 خمسة\n6 ستة\n7 سبعة\n8 ثمانية\n9 تسعة\n10 عشرة\n11 أحد عشر\n12 اثنا عشر\n13 ثلاثة عشر\n14 أربعة عشر\n15 خمسة عشر\n16 ستة عشر\n17 سبعة عشر\n18 ثمانية عشر\n19 تسعة عشر\n20 عشرون',
                'vocab': 'Zahlen=أرقام;eins=واحد;zwei=اثنان;drei=ثلاثة;zwanzig=عشرون',
                'order': 2
            },
            
            # A2 Level Lessons
            {
                'level': 'A2',
                'title': 'العائلة',
                'slug': 'a2-family',
                'youtube_url': 'https://www.youtube.com/watch?v=Zl0iq2HhR6M',
                'content': 'Das ist meine Familie.\nMein Vater ist Lehrer.\nMeine Mutter ist Hausfrau.\nIch habe zwei Brüder und eine Schwester.',
                'translation': 'هذه عائلتي.\nوالدي معلم.\nأمي ربة منزل.\nلدي شقيقان وأخت واحدة.',
                'vocab': 'Familie=عائلة;Vater=أب;Mutter=أم;Bruder=أخ;Schwester=أخت',
                'order': 1
            },
            {
                'level': 'A2',
                'title': 'الأفعال اليومية',
                'slug': 'a2-daily-verbs',
                'youtube_url': 'https://www.youtube.com/watch?v=w1VvI3fSxg0',
                'content': 'Ich stehe um 7 Uhr auf.\nIch frühstücke um halb acht.\nIch gehe um acht Uhr zur Schule.\nIch komme um 14 Uhr nach Hause.',
                'translation': 'أستيقظ في السابعة صباحاً.\nأتناول الإفطار في السابعة والنصف.\nأذهب إلى المدرسة في الثامنة.\nأعود إلى المنزل في الثانية ظهراً.',
                'vocab': 'aufstehen=يستيقظ;frühstücken=يتناول الفطور;zur Schule gehen=يذهب إلى المدرسة;nach Hause kommen=يعود إلى المنزل',
                'order': 2
            },
            
            # B1 Level Lessons
            {
                'level': 'B1',
                'title': 'تصريف الأفعال في الماضي',
                'slug': 'b1-past-tense',
                'youtube_url': 'https://www.youtube.com/watch?v=7_E9jHQpFMs',
                'content': 'Ich ging gestern ins Kino.\nEr hat das Buch gelesen.\nWir haben Pizza gegessen.\nSie ist nach Berlin gefahren.',
                'translation': 'ذهبتُ إلى السينما أمس.\nهو قرأ الكتاب.\nتناولنا البيتزا.\nهي ذهبت إلى برلين.',
                'vocab': 'ging=ذهب;gelesen=قرأ;gegessen=تناول الطعام;gefahren=سافر/ذهب',
                'order': 1
            },
            {
                'level': 'B1',
                'title': 'استخدام Passiv',
                'slug': 'b1-passiv',
                'youtube_url': 'https://www.youtube.com/watch?v=H2qKk0Jq9Hg',
                'content': 'Das Buch wird von mir gelesen. (Präsens)\nDas Buch wurde gelesen. (Präteritum)\nDas Buch ist gelesen worden. (Perfekt)',
                'translation': 'الكتاب يُقرأ من قِبَلي. (المضارع)\nقُرِئَ الكتاب. (الماضي البسيط)\nلقد قُرِئَ الكتاب. (الماضي التام)',
                'vocab': 'wird gelesen=يُقرأ;wurde gelesen=قُرِئ;ist gelesen worden=لقد قُرِئ',
                'order': 2
            },
            
            # B2 Level Lessons
            {
                'level': 'B2',
                'title': 'التعبير عن الرأي',
                'slug': 'b2-expressing-opinions',
                'youtube_url': 'https://www.youtube.com/watch?v=VQf0bDgHeTQ',
                'content': 'Meiner Meinung nach ist Deutsch eine schöne Sprache.\nIch finde, dass das Wetter heute schön ist.\nAus meiner Sicht ist das eine gute Idee.\nIch bin der Ansicht, dass wir mehr üben sollten.',
                'translation': 'في رأيي أن اللغة الألمانية لغة جميلة.\nأعتقد أن الطقس اليوم جميل.\nمن وجهة نظري هذه فكرة جيدة.\nأنا أرى أننا يجب أن نتدرب أكثر.',
                'vocab': 'Meiner Meinung nach=في رأيي;Ich finde=أعتقد;Aus meiner Sicht=من وجهة نظري;Ich bin der Ansicht=أنا أرى',
                'order': 1
            },
            {
                'level': 'B2',
                'title': 'استخدام الجمل الشرطية',
                'slug': 'b2-conditional-sentences',
                'youtube_url': 'https://www.youtube.com/watch?v=8NlZ2-w1n3Y',
                'content': 'Wenn ich Zeit hätte, würde ich nach Deutschland reisen.\nHätte ich mehr Geld, würde ich ein Auto kaufen.\nWenn ich du wäre, würde ich mehr üben.\nHätte ich gewusst, dass du kommst, hätte ich mehr gekocht.',
                'translation': 'لو كان لدي وقت، لسافرت إلى ألمانيا.\nلو كان لدي المزيد من المال، لاشتريت سيارة.\nلو كنت مكانك، لتدربت أكثر.\nلو كنت أعلم أنك قادم، لكنت أعددت المزيد من الطعام.',
                'vocab': 'wenn=إذا/لو;würde=سوف/س;hätte=لو كان لدي;wäre=سأكون',
                'order': 2
            },
            
            # C1 Level Lessons
            {
                'level': 'C1',
                'title': 'التعبير الأكاديمي',
                'slug': 'c1-academic-german',
                'youtube_url': 'https://www.youtube.com/watch?v=4iR-pJXh2Ak',
                'content': 'Die Auswirkungen der Globalisierung auf die Wirtschaft sind vielfältig.\nForschungsergebnisse zeigen, dass die Digitalisierung die Arbeitswelt nachhaltig verändert.\nIn der vorliegenden Studie wird untersucht, inwiefern soziale Medien das Kommunikationsverhalten beeinflussen.',
                'translation': 'تأثيرات العولمة على الاقتصاد متعددة.\nتظهر نتائج الأبحاث أن الرقمنة تغير عالم العمل بشكل مستدام.\nفي هذه الدراسة الحالية، يتم فحص مدى تأثير وسائل التواصل الاجتماعي على سلوك التواصل.',
                'vocab': 'Auswirkungen=تأثيرات;vielfältig=متعدد;nachhaltig=بشكل مستدام;inwiefern=إلى أي مدى',
                'order': 1
            },
            {
                'level': 'C1',
                'title': 'التعبير عن الافتراضات',
                'slug': 'c1-expressing-assumptions',
                'youtube_url': 'https://www.youtube.com/watch?v=GJ6rEfgQk1o',
                'content': 'Es könnte sein, dass das Projekt erfolgreich wird.\nMan nimmt an, dass die Zahlen steigen werden.\nVermutlich wird es morgen regnen.\nEs ist davon auszugehen, dass sich die Situation verbessert.',
                'translation': 'من الممكن أن ينجح المشروع.\nيفترض أن الأرقام سترتفع.\nعلى الأرجح ستمطر غداً.\nمن المتوقع أن تتحسن الأوضاع.',
                'vocab': 'Es könnte sein=من الممكن أن;Man nimmt an=يفترض;Vermutlich=على الأرجح;Es ist davon auszugehen=من المتوقع',
                'order': 2
            },
            
            # C2 Level Lessons
            {
                'level': 'C2',
                'title': 'الكتابة الرسمية',
                'slug': 'c2-formal-writing',
                'youtube_url': 'https://www.youtube.com/watch?v=Z4T6m7x9WfU',
                'content': 'Sehr geehrte Damen und Herren,\n\nhiermit bewerbe ich mich auf die in Ihrer Anzeige ausgeschriebene Position als...\n\nMit freundlichen Grüßen,\nMustafa Ahmed',
                'translation': 'السيدات والسادة المحترمون،\n\nأتقدم بطلبي لشغل الوظيفة المعلن عنها في إعلانكم كـ...\n\nوتفضلوا بقبول فائق الاحترام،\nمصطفى أحمد',
                'vocab': 'Sehr geehrte=عزيزي/عزيزتي;hiermit=أنا أتقدم;ausgeschriebene Position=الوظيفة المعلن عنها;Mit freundlichen Grüßen=وتفضلوا بقبول فائق الاحترام',
                'order': 1
            },
            {
                'level': 'C2',
                'title': 'قراءة النصوص الأدبية',
                'slug': 'c2-literary-texts',
                'youtube_url': 'https://www.youtube.com/watch?v=Q3zJvR9X9oM',
                'content': '„Der Zauberberg" von Thomas Mann ist ein komplexer Roman, der sich mit philosophischen Themen auseinandersetzt. Die Erzählung spielt in einem Sanatorium in den Schweizer Alpen und thematisiert die geistige Verfassung Europas vor dem Ersten Weltkrieg.',
                'translation': 'رواية "الجبل السحري" لتوماس مان هي رواية معقدة تتناول مواضيع فلسفية. تدور أحداث القصة في مصح صحي في جبال الألب السويسرية وتتناول الحالة الفكرية لأوروبا قبل الحرب العالمية الأولى.',
                'vocab': 'komplexer Roman=رواية معقدة;philosophische Themen=مواضيع فلسفية;Sanatorium=مصح صحي;geistige Verfassung=حالة فكرية',
                'order': 2
            }
        ]
        
        # Create or update levels and lessons
        for lesson_data in lessons_data:
            # Get or create the level
            level, created = Level.objects.get_or_create(
                name=lesson_data['level'],
                defaults={
                    'slug': lesson_data['level'].lower(),
                    'description': f'Deutsch Lernen - Niveau {lesson_data["level"]}',
                    'order': ord(lesson_data['level'][1]) - ord('0')  # A1=1, A2=2, etc.
                }
            )
            
            # Create or update the lesson
            lesson, created = Lesson.objects.update_or_create(
                slug=lesson_data['slug'],
                defaults={
                    'title': lesson_data['title'],
                    'level': level,
                    'youtube_url': lesson_data['youtube_url'],
                    'content': lesson_data['content'],
                    'translation': lesson_data.get('translation', ''),
                    'vocab': lesson_data.get('vocab', ''),
                    'order': lesson_data.get('order', 1)
                }
            )
            
            self.stdout.write(self.style.SUCCESS(f'Processed: {level.name} - {lesson.title}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully imported all lessons!'))
