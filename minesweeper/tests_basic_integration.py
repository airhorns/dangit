from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class BasicIntegrationTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_get_index(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertIn('Dangit', self.selenium.title)

    def test_start_new_game(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        new_game_button = self.selenium.find_element_by_css_selector('a[href="/new"]')
        new_game_button.click()
        self.assertIn('New Game', self.selenium.title)

        beginner_button = self.selenium.find_element_by_css_selector('.tile.is-primary button')
        new_game_button.click()
