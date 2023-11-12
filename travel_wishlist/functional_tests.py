from selenium.webdriver.chrome.webdriver import WebDriver

from django.test import LiveServerTestCase

class TitleTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass() # set up live server
        cls.selenium = WebDriver() # interact with web browser 
        cls.selenium.implicitly_wait(10) # wait up to ten seconds

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit() # close browser
        super().tearDownClass # close server

    def test_title_on_home_page(self):
        self.selenium.get(self.live_server_url) # get url
        self.assertIn('Travel Wishlist', self.selenium.title)


class AddPlacesTest(LiveServerTestCase):

    fixtures = ['test_places']

    @classmethod
    def setUpClass(cls):
        super().setUpClass() # set up live server
        cls.selenium = WebDriver() # interact with web browser 
        cls.selenium.implicitly_wait(10) # wait up to ten seconds

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit() # close browser
        super().tearDownClass # close server

    def test_add_new_place(self):
        self.selenium.get(self.live_server_url)
        input_name = self.selenium.find_element('id','id_name') #find_element_by_id() is depreicated. Must use find_element('id', 'name of id')
        input_name.send_keys('Denver')

        add_button = self.selenium.find_element('id','add-new-place')
        add_button.click()

        denver = self.selenium.find_element('id','place-name-5')
        self.assertEqual('Denver', denver.text) # checks text property

        self.assertIn('Denver', self.selenium.page_source) # checks if "Denver" is in the page
        self.assertIn('New York', self.selenium.page_source)
        self.assertIn('Tokyo', self.selenium.page_source)