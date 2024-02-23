import logging
import sys

import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import subprocess



FORMAT = '{levelname:<8} - {asctime}. In modul "{name}", in line {lineno:03d}, funcName "{funcName}()" in {created} sec, message: {msg}'
logging.basicConfig(format=FORMAT, style='{',filename='project.log', filemode='w', level=logging.INFO) # сохранаяю результаты лоиггирования в отдельный файл
logger = logging.getLogger('Final_certification')

with open("./data.yaml") as f:
    data_site = yaml.safe_load(f)

with open("./locators.yaml") as f:
    locators = yaml.safe_load(f)


class Site:
    # проверка на то какой браузер используется в тесте
    def __init__(self, browser, address):
        logger.info('Инициализация теста')
        try:
            self.browser = browser
            self.address = address

            if self.browser == 'chrome':
                logger.info('Browser: chrome')
                self.driver = webdriver.Chrome()
            else:
                logger.critical(f'ERROR! Incorrect Browser')
                sys.exit()

            self.username = data_site['user_name']
            self.passwd = data_site['passwd']

            self.driver.implicitly_wait(data_site['sleep_time'])
            self.driver.get(self.address)
        except BaseException as err:
            logging.exception(f"Критическая ошибка: {err}")
            sys.exit()

    def registration_on_the_website(self):
        """Функция ввода корректных логина и пароля для входа на сайт"""
        logger.info('Enter to the website')
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
        logger.info(f'Find {mode}-element {path}')
        if mode == "css":
            element = self.driver.find_element(By.CSS_SELECTOR, path)
        elif mode == "xpath":
            element = self.driver.find_element(By.XPATH, path)
        else:
            logger.critical(f'ERROR! Incorrect input type')
            sys.exit()
        return element

    def close(self):
        logger.info(f'The end')
        self.driver.close()


def test_step1(site_connect):
    """Проверка на вход в профиль при корректном пароле и логине"""
    # Ищу слово Blog, которое высвечивается после успешном входе
    logger.info(f'Start test1')
    site_connect.registration_on_the_website()
    x_selector1 = locators['LOCATOR_WORD_BLOCK']
    flag_text_blog = site_connect.find_element("xpath", x_selector1)
    site_connect.driver.implicitly_wait(data_site['sleep_time'])
    assert flag_text_blog.text == "Blog", "Faile Test1 (Fine word Blog)"

def test_step2(site_connect):
    """Проверка размера шрифта в заголовке открывшегося окна"""
    logger.info(f'Start test2')
    x_btn_about = locators['LOCATOR_BOTTOM_ABOUT']
    btn = site_connect.find_element("xpath", x_btn_about)
    btn.click()

    x_text = locators['LOCATOR_LABEL_ABOUT_PAGE'] # нахожу заголовок ABOUT PAGE
    label_about = site_connect.find_element("xpath", x_text)
    site_connect.driver.implicitly_wait(data_site['sleep_time'])
    # возможно надо label_about.execute_script
    font_size_of_about_page = label_about.value_of_css_property('font-size')

    assert font_size_of_about_page == '32px', "Faile Test2 (Size of About page)"

def test_step3(command_nikto):
    """Тест на безопасность соединения"""

    result = str(subprocess.run(command_nikto, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    assert '0 error(s)' in result



