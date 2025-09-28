from django.db import migrations, models
import django.db.models.deletion

def set_default_user_profile(apps, schema_editor):
    """Set default user profile for existing UserFlashcardProgress records"""
    UserProfile = apps.get_model('courses', 'UserProfile')
    UserFlashcardProgress = apps.get_model('courses', 'UserFlashcardProgress')
    
    # Get or create a default user profile (you might need to adjust this)
    default_profile = UserProfile.objects.first()
    if default_profile:
        UserFlashcardProgress.objects.filter(user_profile__isnull=True).update(
            user_profile=default_profile
        )

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_userprofile_flashcarddeck_flashcard_discussion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userflashcardprogress',
            name='user_profile',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='flashcard_progress',
                to='courses.userprofile',
                null=True  # Make it nullable first
            ),
        ),
        migrations.RunPython(set_default_user_profile, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='userflashcardprogress',
            name='user_profile',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='flashcard_progress',
                to='courses.userprofile',
                null=False  # Now make it non-nullable
            ),
        ),
    ]
