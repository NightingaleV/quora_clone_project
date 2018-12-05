from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path=r'D:\02__Websites\_Tools\chromedriver.exe')
        # Wait 2 secs for next action
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def browset_close_down(self):
        self.browser.quit()

    def test_start_app(self):
        # Goto App Index
        self.browser.get('http://localhost:3000')
        # Check page title
        self.assertIn('Quora', self.browser.title)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
