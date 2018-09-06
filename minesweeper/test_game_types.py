
from django.test import TestCase
from minesweeper.models import GAME_TYPES


beginner = GAME_TYPES[0]


class GameTypesTestCase(TestCase):
    def test_adjacent_positions_for_square_beginner_game(self):
        self.assertCountEqual([1, 8, 9], beginner.adjacent_positions[0])
        self.assertCountEqual([6, 14, 15], beginner.adjacent_positions[7])
        self.assertCountEqual([48, 49, 57], beginner.adjacent_positions[56])
        self.assertCountEqual([54, 55, 62], beginner.adjacent_positions[63])

        self.assertCountEqual([32, 33, 41, 48, 49], beginner.adjacent_positions[40])
        self.assertCountEqual([22, 23, 30, 38, 39], beginner.adjacent_positions[31])

        self.assertCountEqual([11, 12, 13, 19, 21, 27, 28, 29], beginner.adjacent_positions[20])
