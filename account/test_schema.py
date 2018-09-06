from django.test import TestCase, RequestFactory
from dangit.schema import schema


class SchemaTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_register_mutation_success(self):
        request = self.factory.request()
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
        request = self.factory.request()
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
