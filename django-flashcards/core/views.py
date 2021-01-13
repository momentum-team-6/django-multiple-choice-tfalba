from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.urls import reverse
from django.http import JsonResponse
from .models import User, Deck, Card
from .forms import DeckForm, CardForm
import json
import random
import requests

@login_required
def index(request):
  decks = Deck.objects.all()
  return render(request, 'decks/index.html', {"decks": decks})

@login_required
def search_add(request, deck_pk):
  deck = get_object_or_404(Deck, pk=deck_pk)
  return render(request, 'decks/cards/search_add_card.html', {"deck": deck})

@login_required
def deck_detail(request, deck_pk):
  deck = get_object_or_404(Deck, pk=deck_pk)
  #cards = Card.objects.filter(deck=deck)
  return render(request, 'decks/deck_detail.html', {"deck": deck})

@login_required
def add_deck(request):
  if request.method == 'GET':
    form = DeckForm()
  else:
    form = DeckForm(request.POST, request.FILES)
    if form.is_valid():
      # breakpoint()
      new_deck = form.save(commit=False)
      new_deck.user = request.user
      new_deck.save()

      return redirect(to='home')
  return render(request, "decks/add_deck.html", {"form": form })

@login_required
def card_detail(request, pk):
  card = get_object_or_404(Card, pk=pk)
  return render(request, 'decks/cards/card_detail.html', {"card": card})

# add separate view for add card from search -- this goes into the fetch request
@login_required
def ajax_add_card(request, deck_pk):
  answer = json.load(request)['answer']
  question_image = json.load(request)['question_image']

  
  new_card = Card.objects.create(question_image=question_image, answer=answer)
  #data = {'add': 'new-card'}
  return redirect(to='deck-detail', deck_pk=deck_pk)


@login_required
def add_card(request, deck_pk):
  deck = get_object_or_404(Deck, pk=deck_pk)
  cards = Card.objects.filter(deck=deck)
  if request.method == 'GET':
    form = CardForm()
  else:
    form = CardForm(data=request.POST)
    if form.is_valid():
      new_card = form.save(commit=False)
      new_card.deck = deck
      new_card.save()
      return redirect(to='deck-detail', deck_pk=deck_pk)
  return render(request, "decks/cards/add_card.html", {"deck": deck, "form": form, "cards": cards})


@login_required
def random_card(request, deck_pk):
  deck = get_object_or_404(Deck, pk=deck_pk)
#  cards = Card.objects.filter(deck=deck)
  cards = Card.objects.filter(answered='False', deck=deck)
  card = cards.order_by("?").first()
  return redirect(to='card-detail', pk=card.id)
  
@login_required
def mark_correct(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if not card.answered:
      card.answered = True
      card.save()
      data = {'change': 'correct'}
    else:
      card.answered = False
      card.save()
      data = {'change': 'not-correct'}
    return JsonResponse(data)

@login_required
def start_round(request, deck_pk):
  deck = get_object_or_404(Deck, pk=deck_pk)
  cards = Card.objects.filter(deck=deck)
  for card in cards:
    if card.answered == True:
      card.answered = False
      card.save()
  return redirect(to='random-card', deck_pk=deck.pk)

