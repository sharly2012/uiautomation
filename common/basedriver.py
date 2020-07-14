#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Samuel

import os
from selenium import webdriver
from common.logger import logger
from common.baseutil import root_path, get_yaml_value, get_config_value
from selenium.webdriver.chrome.options import Options
from settings import *

system_name = get_config_value('Driver', 'system')
logger.info("当前系统为" + system_name)
browser = get_yaml_value('Driver', 'browser')
logger.info("选择的浏览器为: %s 浏览器" % browser)

if system_name == 'Linux':
    chrome_driver_path = os.path.join(root_path, 'driver', 'Linux', 'chromedriver')
elif system_name == 'MacOS':
    chrome_driver_path = os.path.join(root_path, 'driver', 'MacOS', 'chromedriver')
elif system_name == 'Windows':
    chrome_driver_path = os.path.join(root_path, 'driver', 'Windows', 'chromedriver.exe')
else:
    raise Exception('操作系统名字错误')


def open_browser():
    options = Options()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': os.path.join(root_path, 'files')}
    options.add_experimental_option('prefs', prefs)
    options.add_argument('-–start-maximized')
    options.add_argument('--window-size=1920,1080')
    if system_name == 'Linux':
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    if proxy_server:
        options.add_argument('--proxy-server=prepub.proxy.moseeker.com:58000')
    driver = webdriver.Chrome(chrome_driver_path, options=options)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(10)
    logger.info("Open browser successfully")
    driver.get(base_url)
    return driver
