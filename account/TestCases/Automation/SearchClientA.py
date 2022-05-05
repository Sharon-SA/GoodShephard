import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):
        user = "instructor"
        pwd = "gounomavs1a"
        search="a"
        driver = self.driver
        driver.maximize_window()
        driver.get("http://foodpantry.pythonanywhere.com/")
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"id_username\"]").send_keys(user)
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"id_password\"]").send_keys(pwd)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/p[3]/input").click()
        time.sleep(1)
        # assert "Logged in"
        # search bar
        driver.find_element_by_xpath("/html/body/div[2]/div/form/input[2]").send_keys(search)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/div/form/button").click()
        time.sleep(3)




def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()
