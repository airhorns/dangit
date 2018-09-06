from random import randint
from minesweeper.models import game_type_for_name, GameState


def generate_minemap(rows, columns, mines):
    positions = rows * columns
    mine_locations = set()
    while len(mine_locations) != mines:
        mine_locations.add(randint(0, positions - 1))

    mine_locations = list(mine_locations)
    mine_locations.sort()
    return mine_locations


def start_game(user, game_type_name):
    game_type = game_type_for_name(game_type_name)
    game_state = GameState(
        owning_player=user,
        game_type=game_type.name,
        open=True,
        won=None,
        minemap=generate_minemap(game_type.rows, game_type.columns, game_type.mines),
        openmap=[],
        flagmap=[],
    )

    game_state.save()
    return True, game_state
