# Generated by Django 5.1.4 on 2025-01-06 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=254, unique=True),
        ),
    ]
