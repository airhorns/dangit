from django.test import TestCase
from minesweeper.models import game_type_for_name, Board, InvalidPositionException, AlreadyRevealedException

beginner = game_type_for_name('beginner')
hexagonal = game_type_for_name('hexagonal')


class BoardTestCase(TestCase):
    def test_can_be_built_from_a_minemap(self):
        board = Board(beginner, [1, 2, 3])
        self.assertIsNone(board.won())

    def test_can_be_built_from_a_minemap_openmap_and_flagmap(self):
        board = Board(beginner, [1, 2, 3], [0, 4], [1])
        self.assertIsNone(board.won())

    def test_opening_a_mine_loses_the_game(self):
        board = Board(beginner, [1, 2, 3], [])
        self.assertIsNone(board.won())

        board = board.open(1)
        self.assertFalse(board.won())

    def test_opening_all_but_the_mines_wins_the_game(self):
        board = Board(beginner, [1, 2, 3], (i for i in range(4, 64)))
        self.assertIsNone(board.won())

        board = board.open(0)
        self.assertTrue(board.won())

    def test_opening_an_invalid_position_raises_an_exception(self):
        board = Board(beginner, [1, 2, 3], [])
        with self.assertRaises(InvalidPositionException):
            board.open(-1)

        with self.assertRaises(InvalidPositionException):
            board.open(100000)

    def test_opening_a_flagged_position_removes_the_flag_from_the_position(self):
        board = Board(beginner, [1, 2, 3], [])

        board = board.toggle_flag(20)
        self.assertCountEqual([20], board.flagmap)

        board = board.open(20)
        self.assertCountEqual([], board.flagmap)

    def test_opening_an_position_adjacent_to_mines_doesnt_autoopen_other_positions(self):
        board = Board(beginner, [1, 2, 3], [])
        self.assertGreater(board.adjacent_mine_count(4), 0)
        board = board.open(4)
        self.assertCountEqual([4], board.openmap)

    def test_opening_space_with_a_corner_mine(self):
        #  M  1  x  x  x  x  x  x
        #  1  1  x  x  x  x  x  x
        #  x  x  x  x  x  x  x  x
        board = Board(beginner, [0], [])
        self.assertEqual(0, board.adjacent_mine_count(5))

        board = board.open(5)
        expected_openmap = set((i for i in range(64))).difference([0])
        self.assertCountEqual(expected_openmap, board.openmap)

    def test_opening_space_with_a_mine_island(self):
        #  x  x  x  x  x  x  x  x
        #  x  x  1  2  2  1  x  x
        #  x  x  1  M  M  1  x  x
        #  x  x  1  2  2  1  x  x
        #  x  x  x  x  x  x  x  x
        board = Board(beginner, [19, 20], [])
        self.assertEqual(0, board.adjacent_mine_count(0))

        board = board.open(0)
        expected_openmap = set((i for i in range(64))).difference([19, 20])
        self.assertCountEqual(expected_openmap, board.openmap)

    def test_opening_space_with_some_side_mines(self):
        #  H  M  M  M  1  x  x  x
        #  1  2  3  2  1  x  x  x
        #  x  x  x  x  x  x  x  x
        # The top left corner isn't reachable from the open space, so it shouldn't be opened
        board = Board(beginner, [1, 2, 3], [])
        self.assertEqual(0, board.adjacent_mine_count(5))

        board = board.open(5)
        expected_openmap = set((i for i in range(64))).difference([0, 1, 2, 3])
        self.assertCountEqual(expected_openmap, board.openmap)

    def test_adjacent_mine_counts_with_a_corner_mine(self):
        #  M  1  x  x  x  x  x  x
        #  1  1  x  x  x  x  x  x
        #  x  x  x  x  x  x  x  x
        board = Board(beginner, [0], []).open(5)

        self.assertCountEqual({1: 1, 8: 1, 9: 1}, board.adjacent_mine_counts_for_openmap())

    def test_adjacent_mine_counts_with_a_mine_island(self):
        #  x  x  x  x  x  x  x  x
        #  x  x  1  2  2  1  x  x
        #  x  x  1  M  M  1  x  x
        #  x  x  1  2  2  1  x  x
        #  x  x  x  x  x  x  x  x
        board = Board(beginner, [19, 20], []).open(0)
        self.assertCountEqual({10: 1, 11: 2, 12: 2, 13: 1, 18: 1, 21: 1, 26: 1, 27: 2, 28: 2, 29: 1}, board.adjacent_mine_counts_for_openmap())

    def test_adjacent_mine_counts_with_some_side_mines(self):
        #  H  M  M  M  1  x  x  x
        #  1  2  3  2  1  x  x  x
        #  x  x  x  x  x  x  x  x
        # The top left corner isn't reachable from the open space, so it shouldn't be opened
        board = Board(beginner, [1, 2, 3], []).open(5)
        self.assertCountEqual({4: 1, 8: 1, 9: 2, 10: 3, 11: 2, 12: 1}, board.adjacent_mine_counts_for_openmap())

    def test_flagging_a_position_adds_it_to_the_flagmap_or_removes_it_if_its_already_inside(self):
        board = Board(beginner, [1, 2, 3])
        self.assertCountEqual([], board.flagmap)

        board = board.toggle_flag(1)
        self.assertCountEqual([1], board.flagmap)

        board = board.toggle_flag(4)
        self.assertCountEqual([1, 4], board.flagmap)

        board = board.toggle_flag(1)
        self.assertCountEqual([4], board.flagmap)

    def test_flagging_an_invalid_position_raises(self):
        board = Board(beginner, [1, 2, 3])
        with self.assertRaises(InvalidPositionException):
            board.toggle_flag(-1)

    def test_flagging_an_open_position_raises(self):
        board = Board(beginner, [1, 2, 3], [4])
        with self.assertRaises(AlreadyRevealedException):
            board.toggle_flag(4)

    def test_adjacent_mine_count_for_empty_squares(self):
        board = Board(beginner, [1, 2, 3])
        self.assertEqual(0, board.adjacent_mine_count(63))

    def test_adjacent_mine_count_for_squares_near_mines(self):
        board = Board(beginner, [1, 2, 3])
        self.assertEqual(3, board.adjacent_mine_count(10))
        self.assertEqual(2, board.adjacent_mine_count(11))
        self.assertEqual(2, board.adjacent_mine_count(9))
        self.assertEqual(1, board.adjacent_mine_count(0))
        self.assertEqual(1, board.adjacent_mine_count(4))


class HexagonalBoardTestCase(TestCase):
    def test_adjacent_mine_count_for_corner_mines(self):
        # M   1   x   x   x
        #   1   x   x   x   x
        # x   x   x   x   x
        board = Board(hexagonal, [0])
        self.assertEqual(1, board.adjacent_mine_count(1))
        self.assertEqual(0, board.adjacent_mine_count(2))
        self.assertEqual(1, board.adjacent_mine_count(24))
        self.assertEqual(0, board.adjacent_mine_count(25))
        self.assertEqual(0, board.adjacent_mine_count(48))

    def test_adjacent_mine_count_for_mine_islands(self):
        # x   x   x   x   x
        #   x   1   1   x   x
        # x   1   M   1   x
        #   x   1   1   x   x
        # x   x   x   x   x
        board = Board(hexagonal, [50])
        # above
        self.assertEqual(0, board.adjacent_mine_count(24))
        self.assertEqual(1, board.adjacent_mine_count(25))
        self.assertEqual(1, board.adjacent_mine_count(26))
        self.assertEqual(0, board.adjacent_mine_count(27))
        # mine row
        self.assertEqual(0, board.adjacent_mine_count(48))
        self.assertEqual(1, board.adjacent_mine_count(49))
        self.assertEqual(1, board.adjacent_mine_count(51))
        self.assertEqual(0, board.adjacent_mine_count(52))
        # below
        self.assertEqual(0, board.adjacent_mine_count(72))
        self.assertEqual(1, board.adjacent_mine_count(73))
        self.assertEqual(1, board.adjacent_mine_count(74))
        self.assertEqual(0, board.adjacent_mine_count(75))

    def test_adjacent_mine_count_for_high_mine_cells(self):
        # x   x   x   x   x
        #   x   1   2   1   x
        # x   1   M   M   2
        #   x   2   4   M   x
        # x   1   M   M   2
        board = Board(hexagonal, [50, 51, 75, 98, 99])
        self.assertEqual(5, board.adjacent_mine_count(74))
        self.assertEqual(2, board.adjacent_mine_count(26))
        self.assertEqual(2, board.adjacent_mine_count(73))
        self.assertEqual(1, board.adjacent_mine_count(97))
