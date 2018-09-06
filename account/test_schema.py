from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from dangit.schema import schema


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

    def test_register_mutation_success(self):
        request = self.request()
        query = """
        mutation {
          register(
                email: "coolcat@fellow.co",
                password: "123abc123",
            )
          {
            ok
            errors
          }
        }
        """

        expectation = {
            'register': {
                'ok': True,
                'errors': None
            }
        }
        result = schema.execute(query, context_value=request)
        self.assertIsNone(result.errors)
        self.assertEqual(result.data, expectation)

    def test_register_mutation_nonunique_email(self):
        request = self.request()
        query = """
        mutation {
          register(
                email: "coolcat@fellow.co",
                password: "123abc123",
            )
          {
            ok
            errors
          }
        }
        """

        expectation = {
            'register': {
                'ok': False,
                'errors': ['email', 'Email already registered.']
            }
        }
        # execute once to create user
        result = schema.execute(query)
        self.assertTrue(result.data['register']['ok'])

        # execute again to trigger duplicate email
        result = schema.execute(query, context_value=request)
        self.assertIsNone(result.errors)
        self.assertEqual(result.data, expectation)

    def test_login_mutation_success(self):
        request = self.request()
        query = """
        mutation {
            login(
                email: "testuser@dangit.ca",
                password: "dangit123"
            ) {
                ok
                errors
                user {
                    email
                }
            }
        }
        """

        result = schema.execute(query, context_value=request)
        self.assertIsNone(result.data['login']['errors'])
        self.assertEqual(result.data['login']['user']['email'], 'testuser@dangit.ca')

    def test_login_mutation_error(self):
        request = self.request()

        query = """
        mutation {
            login(
                email: "testuser@dangit.ca",
                password: "incorrect"
            ) {
                ok
                errors
                user {
                    email
                }
            }
        }
        """

        result = schema.execute(query, context_value=request)
        result = schema.execute(query, context_value=request)
        self.assertIsNotNone(result.data['login']['errors'])
        self.assertIsNone(result.data['login']['user'])
