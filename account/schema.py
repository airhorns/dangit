import graphene
from graphene_django.types import DjangoObjectType

from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ('password', 'is_superuser', )


class Register(graphene.Mutation):
    """
    Mutation to register a user
    """
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, email, password):
        try:
            user = User.objects.create(email=email, is_active=True)  # cheat, and don't do email activation for now
            user.set_password(password)
            user.save()
            return Register(ok=bool(user.id))
        except Exception:
            errors = ["email", "Email already registered."]
            return Register(ok=False, errors=errors)


class Query(object):
    user = graphene.Field(UserType, description="The currently logged in user, if there is one.")

    def resolve_user(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None


class Mutation(object):
    register = Register.Field()
