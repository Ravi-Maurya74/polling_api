# Generated by Django 4.1.2 on 2022-12-07 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_alter_voter_answered_alter_voter_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
    ]
