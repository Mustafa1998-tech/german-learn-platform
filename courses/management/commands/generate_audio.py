import os
import time
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from gtts import gTTS
from courses.models import Lesson

class Command(BaseCommand):
    help = 'Generate audio files for all lessons using gTTS'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force regenerate audio files even if they already exist',
        )
        parser.add_argument(
            '--lesson-id',
            type=int,
            help='Generate audio for a specific lesson ID',
        )
    
    def handle(self, *args, **options):
        force = options['force']
        lesson_id = options['lesson_id']
        
        # Create audio directory if it doesn't exist
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
        os.makedirs(audio_dir, exist_ok=True)
        
        # Get lessons to process
        if lesson_id:
            lessons = Lesson.objects.filter(id=lesson_id)
            if not lessons.exists():
                self.stdout.write(self.style.ERROR(f'Lesson with ID {lesson_id} does not exist.'))
                return
        else:
            lessons = Lesson.objects.all()
        
        total_lessons = lessons.count()
        processed = 0
        skipped = 0
        errors = 0
        
        self.stdout.write(self.style.SUCCESS(f'Processing {total_lessons} lessons...'))
        
        for lesson in lessons:
            try:
                # Create level directory if it doesn't exist
                level_dir = os.path.join(audio_dir, lesson.level.slug)
                os.makedirs(level_dir, exist_ok=True)
                
                # Set file path
                audio_file = os.path.join(level_dir, f'{lesson.slug}.mp3')
                
                # Skip if file exists and not forcing regeneration
                if os.path.exists(audio_file) and not force:
                    self.stdout.write(
                        self.style.WARNING(f'Skipping lesson {lesson.id} - {lesson.title} (audio already exists)'))
                    skipped += 1
                    continue
                
                # Generate audio using gTTS
                self.stdout.write(f'Generating audio for lesson {lesson.id} - {lesson.title}...')
                
                # Clean the text (remove HTML tags, etc.)
                import re
                clean_text = re.sub('<[^<]+?>', '', lesson.content)  # Remove HTML tags
                clean_text = clean_text.replace('&nbsp;', ' ')  # Replace HTML spaces
                clean_text = ' '.join(clean_text.split())  # Normalize whitespace
                
                # Split text into chunks of 5000 characters (gTTS limit is 5000)
                max_chunk_size = 4500  # Slightly less to be safe
                chunks = [clean_text[i:i+max_chunk_size] for i in range(0, len(clean_text), max_chunk_size)]
                
                # Generate audio for each chunk and combine
                audio_files = []
                for i, chunk in enumerate(chunks):
                    try:
                        tts = gTTS(text=chunk, lang='de', slow=False)
                        chunk_file = f"{audio_file}.part{i}"
                        tts.save(chunk_file)
                        audio_files.append(chunk_file)
                        time.sleep(1)  # Be nice to the API
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'Error generating chunk {i+1} for lesson {lesson.id}: {str(e)}'))
                        raise
                
                # Combine audio files if there are multiple chunks
                if len(audio_files) > 1:
                    from pydub import AudioSegment
                    
                    combined = AudioSegment.empty()
                    for file in audio_files:
                        sound = AudioSegment.from_mp3(file)
                        combined += sound
                        os.remove(file)  # Clean up chunk file
                    
                    combined.export(audio_file, format="mp3")
                elif audio_files:
                    # Only one chunk, just rename it
                    os.rename(audio_files[0], audio_file)
                
                # Update the lesson with the audio file path
                lesson.audio_file = os.path.join('audio', lesson.level.slug, f'{lesson.slug}.mp3')
                lesson.save()
                
                processed += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully generated audio for lesson {lesson.id}'))
                
            except Exception as e:
                errors += 1
                self.stdout.write(
                    self.style.ERROR(f'Error processing lesson {lesson.id}: {str(e)}'))
                # If there was an error, clean up any partial files
                if 'audio_file' in locals() and os.path.exists(audio_file):
                    try:
                        os.remove(audio_file)
                    except:
                        pass
        
        # Print summary
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('Audio generation complete!'))
        self.stdout.write(f'Processed: {processed}')
        self.stdout.write(f'Skipped (already exists): {skipped}')
        self.stdout.write(f'Errors: {errors}')
