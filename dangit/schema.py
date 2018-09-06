import graphene
import minesweeper.schema
import account.schema


class Query(minesweeper.schema.Query, account.schema.Query, graphene.ObjectType):
    pass


class Mutation(minesweeper.schema.Mutation, account.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
