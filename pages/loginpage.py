#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Samuel

from pages.basepage import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):

    def __init__(self, driver):
        super(LoginPage, self).__init__(driver)

    def page_confirm(self):
        self.is_visibility(self.mobile)

    # 手机号输入框
    mobile = (By.XPATH, "//input[@placeholder='手机号']")
    # 密码输入框
    password = (By.XPATH, "//input[@placeholder='密码']")
    # 登录按钮
    login_button = (By.XPATH, "//button[contains(., '登录')]")
    # 登录错误提示信息
    error_meg = (By.XPATH, "//form[@name='loginForm']/div")

    # 输入手机号
    def input_mobile(self, login_mobile):
        self.click(self.mobile)
        self.clear(self.mobile)
        self.send_keys(self.mobile, login_mobile)

    # 输入密码
    def input_password(self, login_password):
        self.click(self.password)
        self.clear(self.password)
        self.send_keys(self.password, login_password)
        self.sleep(2)

    # 点击登录按钮
    def click_login(self):
        self.click(self.login_button)
        self.sleep(5)

    def login(self, mobile, password):
        self.input_mobile(mobile)
        self.input_password(password)
        self.click_login()
