from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_populate_user_profile_in_userflashcardprogress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userflashcardprogress',
            name='user_profile',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='flashcard_progress',
                to='courses.userprofile',
            ),
        ),
    ]
