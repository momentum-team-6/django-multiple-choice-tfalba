# Generated by Django 3.1.5 on 2021-01-12 08:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_deck_deck_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular card across whole library', primary_key=True, serialize=False),
        ),
    ]
