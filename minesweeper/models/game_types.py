from collections import namedtuple


class GameType(namedtuple('GameType', ['name', 'columns', 'rows', 'mines'])):
    __slots__ = ()


GAME_TYPES = [
    GameType(name="beginner", columns=8, rows=8, mines=10),
    GameType(name="intermediate", columns=16, rows=16, mines=40),
    GameType(name="expert", columns=24, rows=24, mines=99)
]


def game_type_for_name(name):
    return next((type for type in GAME_TYPES if type.name == name))
