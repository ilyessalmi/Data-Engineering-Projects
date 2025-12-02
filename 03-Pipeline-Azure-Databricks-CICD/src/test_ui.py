from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest

class UITest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

    def test_title(self):
        driver = self.driver
        driver.get('http://your-web-application-url.com')
        self.assertIn("Expected Title", driver.title)

    def test_element(self):
        driver = self.driver
        driver.get('http://your-web-application-url.com')
        element = driver.find_element(By.ID, 'element-id')
        self.assertIsNotNone(element)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()