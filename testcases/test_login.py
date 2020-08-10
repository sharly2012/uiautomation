import time

import pytest
from pages.loginpage import LoginPage
from pages.homepage import HomePage
from common.baseutil import get_config_value


def test_login(driver):
    login_page = LoginPage(driver)
    login_page.login(get_config_value('MOATS', 'mobile'), get_config_value('MOATS', 'password'))
    homepage = HomePage(driver)
    title = homepage.get_title()
    homepage.get_screen_img()
    assert title == '仟寻移动招聘-招聘管理平台'


def test_baidu(driver):
    driver.get('http://www.baidu.com')
    driver.find_element_by_css_selector('#kw').click()
    driver.find_element_by_css_selector('#kw').send_keys('selenium')
    driver.find_element_by_css_selector('#su')
    time.sleep(5)


if __name__ == '__main__':
    pytest.main(['-s -q', '--browser=chrome', 'test_login.py'])
