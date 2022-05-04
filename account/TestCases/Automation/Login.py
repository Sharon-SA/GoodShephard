import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ll_ATS(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):
        user = "instructor"
        pwd = "gounomavs1a"
        driver = self.driver
        driver.maximize_window()
        driver.get("http://foodpantry.pythonanywhere.com/")
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        time.sleep(7)
        driver.find_element(By.XPATH, "/html/body/div[2]/form/p[3]/input").click()
        time.sleep(7)
        driver.find_element(By.XPATH, "/html/body/div[1]/span[2]/a").click()


def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()
