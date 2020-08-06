import pytest
from pages.loginpage import LoginPage
from pages.homepage import HomePage
from common.baseutil import get_config_value


def test_login(driver):
    login_page = LoginPage(driver)
    login_page.login(get_config_value('MOATS', 'mobile'), get_config_value('MOATS', 'password'))
    homepage = HomePage(driver)
    title = homepage.get_title()
    assert title == '仟寻移动招聘-招聘管理平台'


if __name__ == '__main__':
    pytest.main(['-s -q', '--browser=chrome', 'test_login.py'])
