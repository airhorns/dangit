from collections import namedtuple


def square_adjacency_list(row, column):
    return [
        # Above
        (row - 1, column - 1), (row - 1, column), (row - 1, column + 1),
        # Beside
        (row, column - 1), (row, column + 1),
        # Below
        (row + 1, column - 1), (row + 1, column), (row + 1, column + 1)
    ]


def hexagonal_adjacency_list(row, column):
    # Rows are offset by one in presentation but not in index
    # 0   1   2   3   4
    #   5   6   7   8   9
    # 10  11  12  13  14

    # x   x   x   x   x
    #   x   1   1   x   x
    # x   1   M   1   x
    #   x   1   1   x   x
    # x   x   x   x   x
    column_offset = 0 if row % 2 == 0 else 1

    return [
        # Above left and right
        (row - 1, column - 1 + column_offset), (row - 1, column + column_offset),
        # Beside left and right
        (row, column - 1), (row, column + 1),
        # Below left and right
        (row + 1, column - 1 + column_offset), (row + 1, column + column_offset),
    ]


def position_adjacency_lookup(candidate_generator, rows, columns):
    lookup = {}

    def position(row, column):
        return (row * rows) + column

    def valid(row, column):
        return row >= 0 and row < rows and column >= 0 and column < columns

    for row in range(0, rows):
        for column in range(0, columns):
            candidates = candidate_generator(row, column)
            lookup[position(row, column)] = frozenset(map(
                lambda tup: position(tup[0], tup[1]),
                filter(lambda tup: valid(tup[0], tup[1]), candidates)
            ))

    return lookup


class GameType(namedtuple('GameType', ['name', 'columns', 'rows', 'mines'])):
    def __new__(cls, *args, **kwargs):
        self = super(GameType, cls).__new__(cls, *args, **kwargs)
        if self.name.startswith('hexagonal'):
            adjacency_mapper = hexagonal_adjacency_list
        else:
            adjacency_mapper = square_adjacency_list

        self.adjacent_positions = position_adjacency_lookup(adjacency_mapper, self.rows, self.columns)
        return self

    def total_positions(self):
        return self.rows * self.columns


GAME_TYPES = [
    GameType(name="beginner", columns=8, rows=8, mines=10),
    GameType(name="intermediate", columns=16, rows=16, mines=40),
    GameType(name="expert", columns=24, rows=24, mines=99),
    GameType(name="hexagonal", columns=24, rows=24, mines=99)
]


def game_type_for_name(name):
    return next((type for type in GAME_TYPES if type.name == name))
