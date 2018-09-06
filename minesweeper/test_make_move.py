from django.test import TestCase
from minesweeper.models import GameState, GAME_TYPES
from minesweeper.services import make_move, MoveActionType

beginner = GAME_TYPES[0]


class PlayGameTestCase(TestCase):
    def test_opening_a_cell_in_a_closed_game_has_no_effect(self):
        game_state = GameState(game_type=beginner, minemap=[1, 2, 3])
        game_state.save()

        ok, game_state = make_move(game_state, 1, MoveActionType.OPEN)  # open a mine to end the game
        self.assertTrue(ok)
        self.assertFalse(game_state.open)

        ok, game_state = make_move(game_state, 1, MoveActionType.OPEN)  # try to submit another move
        self.assertFalse(ok)

    def test_opening_a_cell_updates_the_gamestate_with_that_cell_in_the_openmap(self):
        game_state = GameState(game_type=beginner, minemap=[1, 2, 3])
        game_state.save()

        ok, new_game_state = make_move(game_state, 6, MoveActionType.OPEN)
        self.assertIn(6, new_game_state.openmap)  # the actual opened cell
        self.assertIn(7, new_game_state.openmap)  # an autoopened adjacent cell

    def test_flagging_a_cell_toggles_the_gamestate_with_that_cell_in_the_flagmap(self):
        game_state = GameState(game_type=beginner, minemap=[1, 2, 3])
        game_state.save()

        ok, new_game_state = make_move(game_state, 1, MoveActionType.FLAG)
        self.assertTrue(ok)
        self.assertIn(1, new_game_state.flagmap)  # toggles in

        ok, new_game_state = make_move(new_game_state, 1, MoveActionType.FLAG)
        self.assertTrue(ok)
        self.assertNotIn(1, new_game_state.flagmap)  # toggles out

    def test_opening_a_cell_with_a_mine_looses_the_game(self):
        game_state = GameState(game_type=beginner, minemap=[1, 2, 3])
        game_state.save()

        ok, new_game_state = make_move(game_state, 1, MoveActionType.OPEN)
        self.assertTrue(ok)
        self.assertFalse(new_game_state.won)
        self.assertFalse(new_game_state.open)
        self.assertIsNotNone(new_game_state.finished_at)
        self.assertIn(1, new_game_state.openmap)

    def test_opening_all_cells_without_a_mine_wins_the_game(self):
        game_state = GameState(game_type=beginner, minemap=[0])
        game_state.save()

        for i in [1, 2, 8, 9]:
            ok, game_state = make_move(game_state, i, MoveActionType.OPEN)
            self.assertTrue(ok)

        self.assertTrue(game_state.won)
        self.assertFalse(game_state.open)
        self.assertIsNotNone(game_state.finished_at)
        self.assertIn(1, game_state.openmap)
