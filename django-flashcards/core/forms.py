from django import forms
from .models import Deck, Card

class DeckForm(forms.ModelForm):
  class Meta:
    model = Deck
    fields = [
      'name',
      'deck_cover',
      'deck_cover_upload',
      'is_private',
    ]
    

class CardForm(forms.ModelForm):
  class Meta:
    model = Card
    fields = [
      'question_image',
      'question_image_upload',
      'question_text',
      'answer',
    ]



class SearchForm(forms.Form):
  search_term = forms.CharField(label='Search Term', max_length=50, required=False)
