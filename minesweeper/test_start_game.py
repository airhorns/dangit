from django.test import TestCase
from minesweeper.services import start_game
from django.contrib.auth.models import User


class StartGameTestCase(TestCase):
    fixtures = ['users']

    def test_started_games_have_proper_bookkeeping(self):
        user = User.objects.get(pk=1)
        ok, game_state = start_game(user, "beginner")
        self.assertIsNotNone(game_state.pk)
        self.assertEqual(game_state.owning_player, user)
        self.assertEqual(game_state.open, True)
        self.assertIsNone(game_state.won, None)
        self.assertIsNone(game_state.finished_at, None)
        self.assertIsNotNone(game_state.started_at)

    def test_started_games_by_anonymous_users_have_proper_bookkeeping(self):
        ok, game_state = start_game(None, "beginner")
        self.assertIsNotNone(game_state.pk)
        self.assertIsNone(game_state.owning_player)
