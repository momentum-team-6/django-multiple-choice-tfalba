"""flashcards URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),
    path('', views.index, name='home'),
    path('decks/<int:deck_pk>/', views.deck_detail, name='deck-detail'),
    path('decks/', views.add_deck, name='add-deck'),
    path('decks/cards/search_add/<int:deck_pk>', views.search_add, name='search-add'),
    path('decks/cards/<uuid:pk>/', views.card_detail, name='card-detail'),
    path('decks/cards/add/<int:deck_pk>/', views.add_card, name='add-card'),
    path('decks/cards/ajax_add/<int:deck_pk>/', views.ajax_add_card, name='ajax-add-card'),
    path('decks/cards/random_card/<int:deck_pk>/', views.random_card, name='random-card'),
    path('decks/cards/<uuid:pk>/mark_answered', views.mark_correct, name='mark-answered'),
    path('decks/cards/<uuid:pk>/mark_keep_going', views.mark_keep_going, name='mark-keep-going'),
    path('decks/cards/start_round/<int:deck_pk>/', views.start_round, name='start-round'),
    path('decks/<int:user_pk>/color_choice/<int:color_pk>', views.change_color, name='color-choice'),
    path('decks/<int:deck_pk>/edit/', views.edit_deck, name='edit-deck'),
    path('decks/<int:deck_pk>/delete', views.delete_deck, name='delete-deck'),
    path('decks/cards/<uuid:pk>/delete/', views.delete_card, name='delete-card'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns 

    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



