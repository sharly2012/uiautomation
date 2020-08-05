import pytest
from pages.loginpage import LoginPage
from common.baseutil import get_yaml_value


class TestLogin(object):

    def test_login(self, driver):
        login_page = LoginPage(driver)
        login_page.login(get_yaml_value('MOATS', 'mobile'), get_yaml_value('MOATS', 'password'))
        title = login_page.get_title()
        assert title == '仟寻移动招聘-招聘管理平台'


if __name__ == '__main__':
    pytest.main(['-s -q', '--browser=chrome', 'test_login.py'])
