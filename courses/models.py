from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F
import json
from datetime import datetime, timedelta

# Import UserProfile after it's defined to avoid circular imports
UserProfile = None

class Level(models.Model):
    LEVEL_CHOICES = [
        ('A1','A1'),('A2','A2'),('B1','B1'),
        ('B2','B2'),('C1','C1'),('C2','C2')
    ]
    name = models.CharField(max_length=2, choices=LEVEL_CHOICES, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Lesson(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Anfänger'),
        ('intermediate', 'Mittelstufe'),
        ('advanced', 'Fortgeschritten'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Titel')
    slug = models.SlugField(unique=True, verbose_name='URL-Slug')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='lessons', verbose_name='Niveau')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner', verbose_name='Schwierigkeitsgrad')
    short_description = models.TextField(blank=True, verbose_name='Kurzbeschreibung')
    content = models.TextField(verbose_name='Inhalt')
    translation = models.TextField(blank=True, verbose_name='Übersetzung')
    vocab = models.TextField(blank=True, help_text='Wörter durch Semikolon getrennt', verbose_name='Vokabeln')
    grammar_points = models.TextField(blank=True, help_text='Grammatikpunkte durch Semikolon getrennt', verbose_name='Grammatikpunkte')
    youtube_url = models.URLField(blank=True, help_text="Unterstützt YouTube-URLs (watch oder embed)", verbose_name='YouTube Video URL')
    audio_file = models.FileField(upload_to='lesson_audio/', blank=True, null=True, verbose_name='Audio-Datei')
    duration_minutes = models.PositiveIntegerField(default=10, verbose_name='Dauer (Minuten)')
    is_free = models.BooleanField(default=True, verbose_name='Kostenlos?')
    is_featured = models.BooleanField(default=False, verbose_name='Hervorgehoben')
    thumbnail = models.ImageField(upload_to='lesson_thumbnails/', blank=True, null=True, verbose_name='Vorschaubild')
    order = models.PositiveIntegerField(default=0, verbose_name='Reihenfolge')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Erstellt am')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Aktualisiert am')
    
    def save(self, *args, **kwargs):
        if self.youtube_url:
            # Convert watch URL to embed URL if needed
            if 'youtube.com/watch' in self.youtube_url:
                video_id = self.youtube_url.split('v=')[1].split('&')[0]
                self.youtube_url = f'https://www.youtube.com/embed/{video_id}'
            # Convert youtu.be URL to embed URL
            elif 'youtu.be/' in self.youtube_url:
                video_id = self.youtube_url.split('youtu.be/')[-1].split('?')[0]
                self.youtube_url = f'https://www.youtube.com/embed/{video_id}'
            # If it's already an embed URL, make sure it's in the correct format
            elif 'youtube.com/embed/' not in self.youtube_url:
                # If it's some other YouTube URL format we don't recognize, clear it
                self.youtube_url = ''
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['level__order', 'order']

    def __str__(self):
        return f"{self.level.name} - {self.title}"
    
    def get_vocab_list(self):
        if not self.vocab:
            return []
        return [v.strip() for v in self.vocab.split(';') if v.strip()]

class Exercise(models.Model):
    TYPE_CHOICES = [
        ('mcq', 'Multiple Choice'),
        ('tf', 'True/False'),
        ('fill', 'Fill in the Blank')
    ]
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    question = models.TextField()
    options = models.TextField(blank=True)  # JSON for MCQ
    answer = models.TextField()
    order = models.IntegerField(default=0)
    explanation = models.TextField(blank=True)

    class Meta:
        ordering = ['order']

    def get_options(self):
        if not self.options:
            return []
        try:
            return json.loads(self.options)
        except json.JSONDecodeError:
            return self.options.split(';')

    def __str__(self):
        return f"{self.lesson.title} - {self.get_type_display()}"

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    score = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    answers = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        user = self.user.username if self.user else 'Anonymous'
        return f"{user} - {self.lesson} - {self.score}%"


class FlashcardDeck(models.Model):
    """A collection of flashcards for a specific level or topic"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='flashcard_decks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.level.name})"

    def card_count(self):
        return self.flashcards.count()


class Flashcard(models.Model):
    """Individual flashcard with German word and its translation"""
    deck = models.ForeignKey(FlashcardDeck, on_delete=models.CASCADE, related_name='flashcards')
    front = models.TextField()  # German word/phrase
    back = models.TextField()   # Translation
    example = models.TextField(blank=True)  # Example usage
    difficulty = models.IntegerField(default=1, choices=[(1, 'Easy'), (2, 'Medium'), (3, 'Hard')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.front} - {self.back}"


# Using string reference to avoid circular import
class UserFlashcardProgress(models.Model):
    """Tracks user's progress with individual flashcards"""
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='flashcard_progress')
    flashcard = models.ForeignKey('Flashcard', on_delete=models.CASCADE)
    next_review = models.DateTimeField(default=datetime.now)
    review_count = models.IntegerField(default=0)
    ease_factor = models.FloatField(default=2.5)  # Used in spaced repetition
    interval = models.IntegerField(default=1)  # Days until next review
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_profile', 'flashcard')
        verbose_name_plural = 'User Flashcard Progress'
        
    def __str__(self):
        return f"{self.user_profile.user.username if hasattr(self, 'user_profile') else 'Unknown'} - {self.flashcard}"
        
    @property
    def user(self):
        return self.user_profile.user if hasattr(self, 'user_profile') else None


class UserProfile(models.Model):
    """Extended user profile with learning statistics"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    points = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    last_active = models.DateField(auto_now=True)
    daily_goal = models.IntegerField(default=5)  # Number of cards to review daily
    achievements = models.ManyToManyField('Achievement', related_name='user_profiles', blank=True)
    
    def update_streak(self):
        """Update user's login streak"""
        today = datetime.now().date()
        if self.last_active < today - timedelta(days=1):
            # Reset streak if not logged in yesterday
            self.streak_days = 1
        elif self.last_active < today:
            # Increment streak if logged in yesterday
            self.streak_days += 1
        self.last_active = today
        self.save()
    
    def add_points(self, points):
        """Add points to user's total"""
        self.points += points
        self.save()
        
        # Check for achievements
        self.check_achievements()
    
    def check_achievements(self):
        """Check and unlock achievements"""
        achievements = Achievement.objects.filter(
            points_required__lte=self.points,
            users__id=self.user.id
        ).exists()
        
        if not achievements:
            # Find and assign new achievements
            new_achievements = Achievement.objects.filter(
                points_required__lte=self.points
            ).exclude(users=self.user)
            
            for achievement in new_achievements:
                achievement.users.add(self.user)
                # Here you could add notification logic

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Achievement(models.Model):
    """Achievements users can earn"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text='Icon class for display')
    points_required = models.IntegerField(default=0)
    users = models.ManyToManyField(User, related_name='achievements', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Discussion(models.Model):
    """Forum discussions for lessons"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.lesson.title}"


class Comment(models.Model):
    """Comments on discussions"""
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_answer = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username} - {self.content[:50]}..."
