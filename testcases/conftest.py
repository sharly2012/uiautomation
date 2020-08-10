#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Samuel

import os
import pytest
from common.logger import logger
from common.baseutil import root_path
from settings import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities

DRIVER_MAPPING = {
    "MacOS": {
        "chrome": "chromedriver",
        "firefox": "geckodriver",
        "safari": "",
        "opera": "operadriver"
    },
    "Linux": {
        "chrome": "chromedriver",
        "firefox": "geckodriver",
        "safari": "",
        "opera": "operadriver"
    },
    "Windows": {
        "chrome": "chromedriver.exe",
        "firefox": "geckodriver.exe",
        "ie": "IEDriverServer.exe",
        "opera": "operadriver.exe"
    }
}


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="browser option: firefox or chrome"
    )
    parser.addoption(
        "--system", action="store", default="MacOS", help="system option: Linux, MacOS or Windows"
    )
    parser.addoption(
        "--server", action="store", default="Production", help="server option: firefox or chrome"
    )


@pytest.fixture(scope='module')
def driver(request):
    system_name = request.config.getoption("--system")
    browser_type = request.config.getoption("--browser")
    environment = request.config.getoption("--server")
    logger.info('Current system name is {}'.format(system_name))
    logger.info('Current browser type is {}'.format(browser_type))
    logger.info('Current environment is {}'.format(environment))
    driver_path = os.path.join(root_path, 'driver', system_name, DRIVER_MAPPING.get(system_name).get(browser_type))
    options = Options()
    # Set the default download folder
    prefs = {
        'profile.default_content_settings.popups': 0,
        'download.default_directory': os.path.join(root_path, 'files')
    }
    options.add_experimental_option('prefs', prefs)
    if system_name == 'Linux':
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    if environment == "Prepub":
        options.add_argument('--proxy-server=%s' % proxy_server)
    # for local test
    # driver = webdriver.Chrome(executable_path=driver_path)
    # driver.set_window_size(1920, 1080)

    # for local selenium server java -jar
    # driver = webdriver.Remote(
    #     command_executor='http://127.0.0.1:4444/wd/hub',
    #     desired_capabilities=DesiredCapabilities.CHROME,
    #     browser_profile=None,
    #     options=options,
    #     keep_alive=True
    # )
    # driver.set_window_size(1920, 1080)

    # just for docker
    driver = webdriver.Remote(
        command_executor='http://10.10.60.88:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME,
    )
    driver.set_window_size(1360, 1020)

    driver.implicitly_wait(30)
    driver.set_page_load_timeout(30)
    driver.get(base_url)

    def close_driver():
        logger.info('All the test cases execute done')
        driver.close()
        driver.quit()

    request.addfinalizer(close_driver)
    return driver


if __name__ == '__main__':
    driver()
