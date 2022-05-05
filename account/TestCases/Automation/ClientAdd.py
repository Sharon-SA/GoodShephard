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
        fname="name1"
        lname="name2"
        dob="01/01/1991"
        gender="Male"
        address="111 1st street"
        city="Wahoo"
        state="NE"
        zip="68066"
        email="test@test.org"
        phone="8675309"
        refby="test"
        refto="test"
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
        # client
        driver.find_element_by_xpath("/html/body/div[1]/ul/li[2]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/div/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/p[1]/input").send_keys(fname)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/p[2]/input").send_keys(lname)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/p[3]/input").send_keys(dob)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/p[4]/input").send_keys(gender)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/p[5]/input").send_keys(address)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/p[6]/input").send_keys(city)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/p[7]/input").send_keys(state)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/p[8]/input").send_keys(zip)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/p[9]/input").send_keys(email)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/p[10]/input").send_keys(phone)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/p[11]/input").send_keys(refby)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/p[12]/input").send_keys(refto)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/button").click()
        time.sleep(1)



def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()
