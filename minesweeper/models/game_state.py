from django.db import models
from django.contrib.auth.models import User
from django.utils.text import capfirst
from .game_types import GAME_TYPES


class GameState(models.Model):
    game_type = models.CharField(max_length=100, choices=((type.name, capfirst(type.name)) for type in GAME_TYPES))
    open = models.BooleanField(default=True)
    won = models.BooleanField(null=True)

    minemap = models.TextField(max_length=10000)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True)

    owning_player = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.slug
