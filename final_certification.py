import sys

import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import json
import requests
from logger import log_all

with open("./data.yaml") as f:
    data_site = yaml.safe_load(f)

with open("./locators.yaml") as f:
    locators = yaml.safe_load(f)


class Site:
    # проверка на то какой браузер используется в тесте
    def __init__(self, browser, address):
        self.browser = browser
        self.address = address

        if self.browser == 'chrome':
            self.driver = webdriver.Chrome()
        else:
            print('Необходимо открыть chrome!')

        self.username = data_site['user_name']
        self.passwd = data_site['passwd']

        self.driver.implicitly_wait(data_site['sleep_time'])
        self.driver.get(self.address)

    def registration_on_the_website(self):
        """Функция ввода корректных логина и пароля для входа на сайт"""

        x_selector1 = locators['LOCATOR_USER_NAME']  # вводим Username
        input1 = self.find_element("xpath", x_selector1)
        input1.send_keys(self.username)

        x_selector2 = locators['LOCATOR_PASSWORD']  # вводим passwd
        input2 = self.find_element("xpath", x_selector2)
        input2.send_keys(self.passwd)

        btn_selector = "button"
        btn = self.find_element("css", btn_selector)
        btn.click()

    def find_element(self, mode, path):
        """Функция поиска элемента на странице сайта по XPATH или CSS"""

        if mode == "css":
            element = self.driver.find_element(By.CSS_SELECTOR, path)
        elif mode == "xpath":
            element = self.driver.find_element(By.XPATH, path)
        else:
            sys.exit()
        return element

    def close(self):
        self.driver.close()


def test_step1(site_connect):
    # Тест при правильном вводе данных пользователя
    # Ищу слово Blog, которое высвечивается после успешной регистрации
    site_connect.registration_on_the_website()
    x_selector1 = locators['LOCATOR_WORD_BLOCK']
    flag_text_blog = site_connect.find_element("xpath", x_selector1)
    site_connect.driver.implicitly_wait(data_site['sleep_time'])
    assert flag_text_blog.text == "Blog"

def test_step2(site_connect):
    """Проверка размера шрифта в заголовке открывшегося окна"""
    x_btn_about = locators['LOCATOR_BOTTOM_ABOUT']
    btn = site_connect.find_element("xpath", x_btn_about)
    btn.click()
    x_text = locators['LOCATOR_LABEL_ABOUT_PAGE']
    label_about = site_connect.find_element("xpath", x_text)
    # возможно надо label_about.execute_script
    print(label_about.text)
