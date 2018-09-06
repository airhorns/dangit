from enum import Enum
from django.utils.timezone import now


class MoveActionType(Enum):
    OPEN = 0
    FLAG = 1


def make_move(game_state, position, action):
    if not game_state.open:
        return False, game_state

    board = game_state.board()
    if action == MoveActionType.OPEN:
        board = board.open(position)
    elif action == MoveActionType.FLAG:
        board = board.toggle_flag(position)
    else:
        raise Exception(f"Unknown action type {action}")

    game_state.openmap = list(board.openmap)
    game_state.flagmap = list(board.flagmap)

    if board.won() is not None:
        game_state.won = board.won()
        game_state.open = False
        game_state.finished_at = now()

    game_state.save()

    return True, game_state
