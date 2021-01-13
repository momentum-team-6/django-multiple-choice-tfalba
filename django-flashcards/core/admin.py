from django.contrib import admin

# Register your models here.
from .models import Deck, Card, User

admin.site.register(Deck)
admin.site.register(Card)
admin.site.register(User)

