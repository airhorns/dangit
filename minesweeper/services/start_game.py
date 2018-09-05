from minesweeper.models import game_type_for_name, GameState


def generate_minemap(rows, columns, mines):
    return ""


def start_game(user, game_type_name):
    game_type = game_type_for_name(game_type_name)
    game_state = GameState(
        owning_player=user,
        game_type=game_type.name,
        open=True,
        won=None,
        minemap=generate_minemap(game_type.rows, game_type.columns, game_type.mines)
    )

    game_state.save()
    return game_state
