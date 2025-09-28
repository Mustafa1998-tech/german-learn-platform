from django.db import migrations

def populate_user_profiles(apps, schema_editor):
    UserProfile = apps.get_model('courses', 'UserProfile')
    UserFlashcardProgress = apps.get_model('courses', 'UserFlashcardProgress')
    
    # Get all UserFlashcardProgress records without a user_profile
    progress_without_profile = UserFlashcardProgress.objects.filter(user_profile__isnull=True)
    
    # Get or create a default user profile
    default_profile = UserProfile.objects.first()
    
    if default_profile:
        # Update all records without a user_profile
        progress_without_profile.update(user_profile=default_profile)
    else:
        # If no profiles exist, we'll need to create one
        User = apps.get_model('auth', 'User')
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            default_profile = UserProfile.objects.create(
                user=admin_user,
                points=0,
                streak_days=0,
                daily_goal=5
            )
            progress_without_profile.update(user_profile=default_profile)


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_add_user_profile_to_userflashcardprogress'),
    ]

    operations = [
        migrations.RunPython(populate_user_profiles, migrations.RunPython.noop),
    ]
