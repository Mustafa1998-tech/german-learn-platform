from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Level, Lesson, UserProfile, Achievement, Result

@receiver(pre_save, sender=Level)
def create_level_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

@receiver(pre_save, sender=Lesson)
def create_lesson_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        instance.slug = f"{instance.level.slug}-{base_slug}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile for each new user"""
    if created:
        UserProfile.objects.create(user=instance)
        
        # Add welcome achievement if it exists
        try:
            welcome_achievement = Achievement.objects.get(name='Welcome to German Learning Platform')
            instance.userprofile.achievements.add(welcome_achievement)
        except Achievement.DoesNotExist:
            pass


@receiver(pre_save, sender=UserProfile)
def update_last_active(sender, instance, **kwargs):
    """Update last active and check streak when user profile is saved"""
    if not instance.pk:
        return  # New profile being created, no need to update streak
    
    try:
        old_instance = UserProfile.objects.get(pk=instance.pk)
        if old_instance.last_active < timezone.now().date():
            instance.update_streak()
    except UserProfile.DoesNotExist:
        pass


@receiver(post_save, sender=Result)
def update_user_progress(sender, instance, created, **kwargs):
    """Update user's points and check for achievements when completing a lesson"""
    if created and instance.user and instance.completed:
        profile = instance.user.userprofile
        points_earned = int(instance.score / 10)  # 10 points per 10% score
        profile.add_points(points_earned)


# Create default achievements if they don't exist
def create_default_achievements():
    """Create default achievements if they don't exist"""
    default_achievements = [
        {
            'name': 'Welcome to German Learning Platform',
            'description': 'You joined the platform!',
            'icon': 'fas fa-star',
            'points_required': 0
        },
        {
            'name': 'First Steps',
            'description': 'Complete your first lesson',
            'icon': 'fas fa-shoe-prints',
            'points_required': 10
        },
        {
            'name': 'Dedicated Learner',
            'description': 'Complete 10 lessons',
            'icon': 'fas fa-graduation-cap',
            'points_required': 100
        },
        {
            'name': 'Vocabulary Master',
            'description': 'Learn 50 words',
            'icon': 'fas fa-book',
            'points_required': 50
        },
        {
            'name': '7-Day Streak',
            'description': 'Use the platform for 7 consecutive days',
            'icon': 'fas fa-fire',
            'points_required': 70
        },
    ]
    
    for achievement_data in default_achievements:
        Achievement.objects.get_or_create(
            name=achievement_data['name'],
            defaults={
                'description': achievement_data['description'],
                'icon': achievement_data['icon'],
                'points_required': achievement_data['points_required']
            }
        )

# Call the function to create default achievements when the app is ready
from django.apps import apps
if apps.is_installed('django.contrib.auth'):
    try:
        create_default_achievements()
    except:
        # Handle case where tables don't exist yet
        pass
