from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path=r'D:\02__Websites\_Tools\chromedriver.exe')
        # Wait 2 secs for next action
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    # def test_start_app(self):
    #     # Goto App Index
    #     self.browser.get('http://localhost:3000')
    #     # Check page title
    #     self.assertIn('Quora', self.browser.title)
    #     # Check Heading
    #     try:
    #         self.browser.find_element_by_tag_name('h1')
    #     except NoSuchElementException:
    #         print('Error: Heading 1 not found')
    #         raise
    #     # Check Navigation
    #     try:
    #         self.browser.find_element_by_tag_name('nav')
    #     except NoSuchElementException:
    #         print('Error: Navigation not found')

    def test_navigation_app(self):
        self.browser.get('http://localhost:3000')
        nav = self.browser.find_element_by_tag_name('nav')
        menu_items = nav.find_elements_by_class_name('menu-link')
        for item in menu_items:
            href = item.get_attribute('href')
            self.browser.get(href)
            self.browser.implicitly_wait(2)
            self.assertNotIn('Page not found', self.browser.title)
            self.browser.back()
            print(href)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
