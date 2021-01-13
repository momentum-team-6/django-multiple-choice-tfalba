from django import forms
from .models import Deck, Card

class DeckForm(forms.ModelForm):
  class Meta:
    model = Deck
    fields = [
      'name',
      'deck_cover',
      'deck_cover_upload',
    ]

    # name = forms.CharField()
    # deck_cover = forms.Textarea()

class CardForm(forms.ModelForm):
  class Meta:
    model = Card
    fields = [
      'question_image',
      'question_image_upload',
      'question_text',
      'answer',
    ]

    # question_image = forms.CharField()
    # question_text = forms.CharField()
    # answer = forms.CharField()

