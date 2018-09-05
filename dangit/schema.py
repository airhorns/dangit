import graphene
import minesweeper.schema


class Query(minesweeper.schema.Query, graphene.ObjectType):
    pass


class Mutation(minesweeper.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
