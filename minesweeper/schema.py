import graphene

from graphene_django.types import DjangoObjectType
from minesweeper.models import GameState, GameMove, game_type_for_name
from minesweeper.services import start_game


class GameTypeType(graphene.ObjectType):
    name = graphene.String()
    columns = graphene.Int()
    rows = graphene.Int()
    mines = graphene.Int()


class GameStateType(DjangoObjectType):
    class Meta:
        model = GameState
        exclude_fields = ('minemap', )

    game_type = graphene.Field(GameTypeType)
    game_type_name = graphene.String()
    won = graphene.Boolean(required=False)

    def resolve_game_type(self, info):
        game_type = game_type_for_name(self.game_type)
        return GameTypeType(name=game_type.name, columns=game_type.columns, rows=game_type.rows, mines=game_type.mines)

    def resolve_game_type_name(self, info):
        return self.game_type


class GameMoveType(DjangoObjectType):
    class Meta:
        model = GameMove


class StartGame(graphene.Mutation):
    class Arguments:
        gameType = graphene.String()

    ok = graphene.Boolean()
    game_state = graphene.Field(lambda: GameStateType)

    def mutate(self, info, gameType):
        user = info.context.user if info.context.user.is_authenticated else None
        game_state = start_game(user=user, game_type_name=gameType)
        ok = True
        return StartGame(game_state=game_state, ok=ok)


class Query(object):
    game_state = graphene.Field(GameStateType, id=graphene.Int())
    all_game_states = graphene.List(GameStateType)

    def resolve_all_game_states(self, info):
        return GameState.objects.all()

    def resolve_game_state(self, info, id):
        return GameState.objects.get(pk=id)


class Mutation(object):
    start_game = StartGame.Field()
