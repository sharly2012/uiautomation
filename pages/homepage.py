#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Samuel

from pages.basepage import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    # 左侧工具栏图标
    moseeker_icon = (By.XPATH, "//div[@class='Sidebar-logo-wrapper']")
    # 左侧工具栏
    left_sidebar = (By.XPATH, "//nav")
    # 职位管理工具栏
    menu_position = (By.XPATH, "//a[contains(@href, '/admin/position')]")
    # user title
    welcome_user = (By.XPATH, "//div[@class='user-title']")
    # 更多
    message_more = (By.ID, "tab-more$")
    # 消息内容
    message_detail = (By.XPATH, "//div[contains(@class, 'MessageItem')]")
    # 候选人新增
    add_button = (By.XPATH, "//button[@type='button'][contains(.,'新增')]")
    add_one_candidate = (By.XPATH, "//li[@class='el-dropdown-menu__item'][contains(.,'新增一位候选人')]")
    # 用户图标
    user_icon = (By.XPATH, "//div[@class='user-dropdown el-dropdown']/span")
    logout_button = (By.XPATH, "//div[@class='content red'][contains(text(), '退出')]")

    def verify_login_success(self):
        user_label = self.get_text(self.welcome_user)
        self.verify_in('Hello', user_label)

    def get_cur_title(self):
        self.get_title()

    # 获取左侧工具栏的全部text
    def get_sidebar_text(self):
        self.get_text(self.left_sidebar)

    def logout(self):
        self.move_to_element(self.user_icon)
        self.sleep(1)
        self.click(self.logout_button)
