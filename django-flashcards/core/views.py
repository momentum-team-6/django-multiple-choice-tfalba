from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, Deck, Card
from .forms import DeckForm, CardForm, SearchForm
import json
import random
import requests

@login_required
def index(request):
  if request.method == 'POST':
    form = SearchForm(data=request.POST)
    if form.is_valid():
      my_search_term = form.cleaned_data['search_term']
      decks = Deck.objects.filter(Q(cards__answer__icontains=my_search_term) | Q(name__icontains=my_search_term)).filter(Q(user=request.user) | Q(is_private=False)).distinct()
  else:
    form = SearchForm()
    decks= Deck.objects.filter(Q(user=request.user) | Q(is_private=False)).distinct()
  return render(request, 'decks/index.html', {"decks": decks, "form": form})

@login_required
def search_add(request, deck_pk):
  deck = get_object_or_404(Deck, pk=deck_pk)
  return render(request, 'decks/cards/search_add_card.html', {"deck": deck})

@login_required
def deck_detail(request, deck_pk):
  deck = get_object_or_404(Deck, pk=deck_pk)
  return render(request, 'decks/deck_detail.html', {"deck": deck})

@login_required
def add_deck(request):
  decks= Deck.objects.filter(Q(user=request.user) | Q(is_private=False))
  if request.method == 'GET':
    form = DeckForm()
  else:
    form = DeckForm(request.POST, request.FILES)
    if form.is_valid():
      new_deck = form.save(commit=False)
      new_deck.user = request.user
      new_deck.save()

      return redirect(to='home')
  return render(request, "decks/add_deck.html", {"form": form, "decks":decks })

@login_required
def card_detail(request, pk):
  card = get_object_or_404(Card, pk=pk)
  return render(request, 'decks/cards/card_detail.html', {"card": card})

@login_required
def ajax_add_card(request, deck_pk):
  response = json.load(request)
  answer = response['answer']
  question_image = response['question_image']
  new_card = Card.objects.create(question_image=question_image, answer=answer, deck_id=deck_pk)
  data = {'status': 'OK'}
  return JsonResponse(data)

@login_required
def add_card(request, deck_pk):
  deck = get_object_or_404(Deck, pk=deck_pk)
  cards = Card.objects.filter(deck=deck)
  if request.method == 'GET':
    form = CardForm()
  else:
    form = CardForm(request.POST, request.FILES)
    if form.is_valid():
      new_card = form.save(commit=False)
      new_card.deck = deck
      new_card.save()
      return redirect(to='deck-detail', deck_pk=deck_pk)
  return render(request, "decks/cards/add_card.html", {"deck": deck, "form": form, "cards": cards})


@login_required
def random_card(request, deck_pk):
  deck = get_object_or_404(Deck, pk=deck_pk)
  cards = Card.objects.filter(answered='False', deck=deck).filter(return_to_pile='False', deck=deck)
  card = cards.order_by("?").first()
  if len(cards) > 0:
    return redirect(to='card-detail', pk=card.id)
  else:
    cards2 = Card.objects.filter(return_to_pile='True', deck=deck)
    card = cards2.order_by("?").first()
    if len(cards2) >0:
      return redirect(to='card-detail', pk=card.id)
    else:
      return redirect(to='deck-detail', deck_pk=deck_pk) 
    return redirect(to='deck-detail', deck_pk=deck_pk)
  
@login_required
def mark_correct(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if not card.answered:
      card.answered = True
      card.return_to_pile = False
      card.save()
      data = {'change': 'correct'}
    else:
      card.answered = False
      card.return_to_pile = False
      card.save()
      data = {'change': 'not-correct'}
    return JsonResponse(data)
  
@login_required
def mark_keep_going(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if not card.answered:
      card.return_to_pile = True
      card.save()
      data = {'change': 'correct'}
    else:
      card.return_to_pile = False
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
    if card.return_to_pile == True:
      card.return_to_pile = False
      card.save()
  return redirect(to='random-card', deck_pk=deck.pk)

@login_required
def change_color(request, user_pk, color_pk):
  user = get_object_or_404(User, id=user_pk)
  user.color = color_pk
  user.save()
  data = {'change to': color_pk}
  return JsonResponse(data)

def edit_deck(request, deck_pk):
  
  deck = get_object_or_404(Deck, id=deck_pk)
  
  if request.method == 'POST':
    
    form = DeckForm(request.POST, request.FILES, instance=deck)
    if form.is_valid():
      form.save()
      return redirect(to='deck-detail', deck_pk=deck_pk)
  else: 
    form = DeckForm(instance=deck)
  return render(request, "decks/edit_deck.html", {
    "form": form,
    "deck": deck
  })

def delete_deck(request, deck_pk):
  deck = get_object_or_404(Deck, id=deck_pk)
  if request.method == 'POST':
    deck.delete()
    return redirect(to='home')
  return render(request, "decks/delete_deck.html", {"deck": deck})


def delete_card(request, pk):
  card = get_object_or_404(Card, id=pk)
  if request.method == 'POST':
    card.delete()
    return redirect(to='edit-deck', deck_pk=card.deck.id)
  return render(request, "decks/cards/delete_card.html", {"card": card})
