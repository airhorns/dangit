import graphene
from graphene_django.types import DjangoObjectType

from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ('password', 'is_superuser', )


class Query(object):
    user = graphene.Field(UserType, description="The currently logged in user, if there is one.")

    def resolve_user(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None


class Mutation(object):
    pass
