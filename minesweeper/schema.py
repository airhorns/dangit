import graphene

from graphene_django.types import DjangoObjectType
from minesweeper.models import GameState, GameMove, game_type_for_name
from minesweeper.services import start_game, make_move, MoveActionType


class AdjacentMineCountType(graphene.ObjectType):
    position = graphene.Int(required=True)
    mines = graphene.Int(required=True)


class BoardType(graphene.ObjectType):
    openmap = graphene.List(graphene.Int, required=True)
    flagmap = graphene.List(graphene.Int, required=True)
    adjacent_mine_counts = graphene.List(AdjacentMineCountType, required=True)

    # GraphQL has no handy dict type, so we need to spit this out as a list of tuples where the
    # fields of each tuple have a name.
    def resolve_adjacent_mine_counts(self, info):
        return [AdjacentMineCountType(position=position, mines=count) for (position, count) in self.adjacent_mine_counts_for_openmap().items()]


class GameTypeType(graphene.ObjectType):
    name = graphene.String(required=True)
    columns = graphene.Int(required=True)
    rows = graphene.Int(required=True)
    mines = graphene.Int(required=True)


MoveActionGraphQLType = graphene.Enum.from_enum(MoveActionType)


class GameStateType(DjangoObjectType):
    class Meta:
        model = GameState
        exclude_fields = ('minemap', 'openmap', 'flagmap')

    game_type = graphene.Field(GameTypeType, required=True)
    game_type_name = graphene.String(required=True)
    won = graphene.Boolean(required=False)
    board = graphene.Field(BoardType, required=True)

    def resolve_game_type(self, info):
        game_type = game_type_for_name(self.game_type)
        return GameTypeType(name=game_type.name, columns=game_type.columns, rows=game_type.rows, mines=game_type.mines)

    def resolve_game_type_name(self, info):
        return self.game_type

    def resolve_board(self, info):
        return self.board()


class GameMoveType(DjangoObjectType):
    class Meta:
        model = GameMove


class StartGame(graphene.Mutation):
    class Arguments:
        gameType = graphene.String(required=True)

    ok = graphene.Boolean(required=True)
    game_state = graphene.Field(GameStateType)

    def mutate(self, info, gameType):
        user = info.context.user if info.context.user.is_authenticated else None
        ok, game_state = start_game(user=user, game_type_name=gameType)
        return StartGame(game_state=game_state, ok=ok)


class MakeMove(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        position = graphene.Int(required=True)
        action = graphene.Argument(MoveActionGraphQLType, required=True)

    ok = graphene.Boolean(required=True)
    game_state = graphene.Field(GameStateType)

    def mutate(self, info, id, position, action):
        game_state = GameState.objects.get(pk=id)

        if game_state.owning_player and game_state.owning_player != info.context.user:
            return MakeMove(False, None)

        ok, game_state = make_move(game_state, position, MoveActionType(action))
        return MakeMove(game_state=game_state, ok=ok)


class Query(object):
    game_state = graphene.Field(GameStateType, id=graphene.Int())
    all_game_states = graphene.List(GameStateType)

    def resolve_all_game_states(self, info):
        return GameState.objects.all()

    def resolve_game_state(self, info, id):
        return GameState.objects.get(pk=id)


class Mutation(object):
    start_game = StartGame.Field()
    make_move = MakeMove.Field()
