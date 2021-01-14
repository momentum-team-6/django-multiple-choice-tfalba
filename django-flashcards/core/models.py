from django.db import models
from django.contrib.auth.models import AbstractUser
from django_random_queryset import RandomManager
import uuid
from django.urls import reverse

class User(AbstractUser):
    COLORS = (
        ('1', 'Mustard'),
        ('2', 'Blue'),
        ('3', 'Red'),
        ('4', 'Green'),
    )

    color = models.CharField(
        max_length=1,
        choices=COLORS,
        blank=True,
        default='1',
        help_text='Color Choice',
    )
    pass

class Deck(models.Model):
    name = models.CharField(max_length=100, help_text='Enter a name to identify your deck. (Required)')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='decks')
    deck_cover = models.CharField(max_length=100, null=True, blank=True, help_text='Enter a url for a deck cover image. (Optioinal)')
    deck_cover_upload = models.ImageField(upload_to = 'images/', blank=True, null=True, help_text='Upload an image for deck cover photo (Optional)')
    is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('deck-detail', args=[str(self.id)])

class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular card across whole library')

    deck = models.ForeignKey('Deck', on_delete=models.CASCADE, related_name='cards')
    question_image = models.CharField(max_length=1000, null=True, blank=True, help_text='Enter a url for question image. (Optioinal)')
    question_image_upload = models.ImageField(upload_to = 'images/', blank=True, null=True, help_text='Upload an image for card question. (Optional)')
    question_text = models.CharField(max_length=1000, null=True, blank=True, help_text='Enter your question in text form. (Optional, Default if no image)')
    answer = models.CharField(max_length=255, help_text='Enter the answer to the question. (Required)')
    answered = models.BooleanField(default=False)
    return_to_pile = models.BooleanField(default=False)
    objects = RandomManager()

    def __str__(self):
        return self.answer

    def get_absolute_url(self):
        return reverse('card-detail', args=[str(self.id)])

