# Generated by Django 4.2.1 on 2023-05-26 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_attemptedtest_is_submitted'),
    ]

    operations = [
        migrations.AddField(
            model_name='optedchoice',
            name='hash',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]