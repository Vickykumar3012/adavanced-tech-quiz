# Generated by Django 4.2 on 2023-04-27 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_attemptedtest_question_marks_optedchoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='optedchoice',
            name='marks',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='optedchoice',
            name='question',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='quiz.question'),
            preserve_default=False,
        ),
    ]
