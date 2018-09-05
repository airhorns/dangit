from django.db import models
from django.contrib.auth.models import User
from .game_state import GameState


class GameMove(models.Model):
    game = models.ForeignKey(GameState, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)

    row = models.IntegerField()
    column = models.IntegerField()
    submitted_at = models.DateTimeField()

    def __str__(self):
        return f"Move at row:{self.row} column:{self.column}"
