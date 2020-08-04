import pytest
from pages.loginpage import LoginPage


class TestLogin(object):

    def test_login(self, driver):
        login_page = LoginPage(driver)
        login_page.login('15000123789', 'moseeker0301')
        title = login_page.get_title()
        assert title == '仟寻移动招聘-招聘管理平台'


if __name__ == '__main__':
    pytest.main(['-s -q', '--browser=chrome', 'test_login.py'])
