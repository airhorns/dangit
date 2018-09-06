from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.utils.text import capfirst
from .game_types import GAME_TYPES, game_type_for_name
from .board import Board


class GameState(models.Model):
    game_type = models.CharField(max_length=100, choices=((type.name, capfirst(type.name)) for type in GAME_TYPES))
    open = models.BooleanField(default=True)
    won = models.BooleanField(null=True)

    minemap = ArrayField(base_field=models.IntegerField())
    openmap = ArrayField(base_field=models.IntegerField(), default=list)
    flagmap = ArrayField(base_field=models.IntegerField(), default=list)

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True)

    owning_player = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)

    def board(self):
        return Board(game_type_for_name(self.game_type), self.minemap, self.openmap, self.flagmap)
