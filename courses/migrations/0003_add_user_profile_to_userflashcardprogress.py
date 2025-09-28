from django.db import migrations, models
import django.db.models.deletion


def add_user_profile_field(apps, schema_editor):
    # This function will add the user_profile field as nullable
    pass  # We'll handle this in the next step


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_userprofile_flashcarddeck_flashcard_discussion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userflashcardprogress',
            name='user_profile',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='flashcard_progress',
                to='courses.userprofile',
            ),
        ),
    ]
