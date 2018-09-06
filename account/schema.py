import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ('password', 'is_superuser', )


class Register(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, email, password):
        request = info.context

        try:
            user = User.objects.create(username=email, email=email, is_active=True)  # cheat, and don't do email activation for now
            user.set_password(password)
            user.save()

            # Auto log the user in since we care more about ease of use than security, and there's no validation step
            if user.id:
                login(request, user)

            return Register(ok=bool(user.id))
        except IntegrityError as e:
            errors = ["email", "Email already registered."]
            return Register(ok=False, errors=errors)


class Login(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    user = graphene.Field(UserType)

    def mutate(self, info, email, password):
        request = info.context
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Login(ok=True, user=user, errors=None)
        else:
            return Login(
                ok=False,
                errors=['email', 'Unable to login with provided credentials.']
            )


class Logout(graphene.Mutation):
    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info):
        if info.context.user.is_authenticated:
            logout(info.context)
            return Logout(ok=True, errors=None)
        else:
            return Logout(ok=False, errors=['none', 'Not logged in.'])


class Query(object):
    user = graphene.Field(UserType, description="The currently logged in user, if there is one.")

    def resolve_user(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None


class Mutation(object):
    register = Register.Field()
    login = Login.Field()
    logout = Logout.Field()
