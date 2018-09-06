from collections import namedtuple


def square_position_adjacency_lookup(rows, columns):
    lookup = {}

    def position(row, column):
        return (row * rows) + column

    def valid(row, column):
        return row >= 0 and row < rows and column >= 0 and column < columns

    for row in range(0, rows):
        for column in range(0, columns):
            candidates = [
                # Above
                (row - 1, column - 1), (row - 1, column), (row - 1, column + 1),
                # Beside
                (row, column - 1), (row, column + 1),
                # Below
                (row + 1, column - 1), (row + 1, column), (row + 1, column + 1)
            ]

            lookup[position(row, column)] = frozenset(map(
                lambda tup: position(tup[0], tup[1]),
                filter(lambda tup: valid(tup[0], tup[1]), candidates)
            ))

    return lookup


class GameType(namedtuple('GameType', ['name', 'columns', 'rows', 'mines'])):
    def __new__(cls, *args, **kwargs):
        self = super(GameType, cls).__new__(cls, *args, **kwargs)
        self.adjacent_positions = square_position_adjacency_lookup(self.rows, self.columns)
        return self

    def total_positions(self):
        return self.rows * self.columns


GAME_TYPES = [
    GameType(name="beginner", columns=8, rows=8, mines=10),
    GameType(name="intermediate", columns=16, rows=16, mines=40),
    GameType(name="expert", columns=24, rows=24, mines=99)
]


def game_type_for_name(name):
    return next((type for type in GAME_TYPES if type.name == name))
