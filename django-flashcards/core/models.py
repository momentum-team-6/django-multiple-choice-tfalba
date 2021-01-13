from django.db import models
from django.contrib.auth.models import AbstractUser
from django_random_queryset import RandomManager
import uuid
from django.urls import reverse

class User(AbstractUser):
    pass

class Deck(models.Model):
    name = models.CharField(max_length=100, help_text='Enter a name to identify your deck')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='decks')
    deck_cover = models.CharField(max_length=100, null=True, blank=True)
    deck_cover_upload = models.ImageField(upload_to = 'images/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular card across whole library')

    deck = models.ForeignKey('Deck', on_delete=models.CASCADE, related_name='cards')
    question_image = models.CharField(max_length=1000, null=True, blank=True)
    question_image_upload = models.ImageField(upload_to = 'images/', blank=True, null=True)
    question_text = models.CharField(max_length=1000, null=True, blank=True)
    answer = models.CharField(max_length=255, help_text='This should be the name of the image')
    answered = models.BooleanField(default=False)
    return_to_pile = models.BooleanField(default=False)
    objects = RandomManager()

    def __str__(self):
        return self.answer

    def get_absolute_url(self):
        return reverse('card-detail', args=[str(self.id)])

