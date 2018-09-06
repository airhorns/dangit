from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from dangit.schema import schema
from minesweeper.models import GameState

User = get_user_model()


class SchemaTestCase(TestCase):
    fixtures = ['users']

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def request(self):
        request = self.factory.request()
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        return request

    def test_start_game_without_a_user(self):
        request = self.request()
        request.user = AnonymousUser()
        query = """
        mutation {
          startGame(gameType: "beginner") {
            ok
            gameState {
                id
            }
          }
        }
        """

        result = schema.execute(query, context_value=request)
        self.assertIsNone(result.errors)
        self.assertEqual(result.data['startGame']['ok'], True)
        self.assertIsNotNone(result.data['startGame']['gameState']['id'])

    def test_start_game_with_a_user(self):
        request = self.request()
        user = User.objects.get(pk=3)
        request.user = user

        query = """
        mutation {
          startGame(gameType: "beginner") {
            ok
            gameState {
                id
            }
          }
        }
        """

        result = schema.execute(query, context_value=request)
        self.assertIsNone(result.errors)
        self.assertEqual(result.data['startGame']['ok'], True)
        self.assertIsNotNone(result.data['startGame']['gameState']['id'])

        game_state = GameState.objects.get(pk=result.data['startGame']['gameState']['id'])
        self.assertEqual(game_state.owning_player, user)

    def test_make_move_on_owned_game(self):
        request = self.request()
        user = User.objects.get(pk=3)
        request.user = user

        query = """
        mutation {
          startGame(gameType: "beginner") {
            ok
            gameState {
                id
            }
          }
        }
        """

        result = schema.execute(query, context_value=request)
        self.assertIsNone(result.errors)
        game_state = GameState.objects.get(pk=result.data['startGame']['gameState']['id'])

        move_query = """
        mutation {
          makeMove(id: %s, position: 0, action: FLAG) {
            ok
            gameState {
                id
            }
          }
        }
        """ % game_state.id
        result = schema.execute(move_query, context_value=request)
        self.assertIsNone(result.errors)
        self.assertEqual(result.data['makeMove']['ok'], True)

    def test_make_move_on_other_users_game_errors(self):
        request = self.request()
        user = User.objects.get(pk=3)
        request.user = user

        query = """
        mutation {
          startGame(gameType: "beginner") {
            ok
            gameState {
                id
            }
          }
        }
        """

        result = schema.execute(query, context_value=request)
        self.assertIsNone(result.errors)
        game_state = GameState.objects.get(pk=result.data['startGame']['gameState']['id'])

        move_query = """
        mutation {
          makeMove(id: %s, position: 0, action: FLAG) {
            ok
            gameState {
                id
            }
          }
        }
        """ % game_state.id
        other_request = self.request()
        other_request.user = AnonymousUser()
        result = schema.execute(move_query, context_value=other_request)
        self.assertIsNone(result.errors)
        self.assertEqual(result.data['makeMove']['ok'], False)

    def test_make_move_on_anonymous_game(self):
        pass
