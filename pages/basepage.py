#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Samuel

import time
import allure
import os
from abc import ABCMeta, abstractmethod
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from common.logger import logger
from common.baseutil import root_path
from unittest import TestCase


def fail_screenshot(func):
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            return result
        except Exception as e:
            logger.info('{} execute appear error: {}'.format(func.__name__, e))
            cur_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            file_name = os.path.join(root_path, 'screenshots', func.__name__ + cur_time + '.png')
            self.driver.get_screenshot_as_file(file_name)
            allure.attach.file(file_name, allure.attachment_type.PNG)
            logger.info('The fail screenshot had been saved in {}'.format(file_name))
            raise Exception(e)

    return wrapper


class BasePage(metaclass=ABCMeta):

    def __init__(self, driver):
        """
        :param driver:打开浏览器驱动
        """
        self.driver: WebDriver = driver
        self.accept_next_alert = True
        self.case = TestCase()
        self.path = root_path
        self.page_confirm()

    @abstractmethod
    def page_confirm(self):
        raise NotImplementedError('请实现确认是否是当前页面的逻辑')

    def open_url(self, url):
        """
        打开URL
        :param url: url
        :return: None
        """
        logger.info("浏览器打开链接: {}".format(url))
        self.driver.get(url)

    def get_title(self):
        """
        获取当前页面的title
        :return: title
        """
        logger.info("当前页面的title为: %s" % self.driver.title)
        return self.driver.title

    @fail_screenshot
    def find_element(self, *locator):
        """
        根据locator查找页面元素
        :param locator: tuple(find_by, value)
        :return: WebElement
        """
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(locator))
            element = self.driver.find_element(*locator)
            return element
        except NoSuchElementException:
            logger.error('Can not find the element: %s' % locator[1])
            raise
        except TimeoutException:
            logger.error('Can not find element: %s in 10 seconds' % locator[1])
            raise

    @fail_screenshot
    def find_elements(self, *locator):
        """
        根据locator查找页面上的所有元素
        :param locator: tuple(find_by, value)
        :return: WebElements
        """
        try:
            elements = WebDriverWait(self.driver, 10, 0.5).until(lambda driver: driver.find_elements(*locator))
            return elements
        except NoSuchElementException:
            logger.error('Can not find the element: %s' % locator[1])
            raise
        except TimeoutException:
            logger.error('Can not find the element: %s in 10 seconds' % locator[1])
            raise

    def get_screen_img(self):
        """
        截图且保存在screenshots目录下
        :return:
        """
        now = time.strftime("%Y-%m-%d_%H_%M_%S")
        file_name = now + '.png'
        screen_path = os.path.join(self.path, 'screenshots', file_name)
        try:
            self.driver.get_screenshot_as_file(screen_path)
            allure.attach.file(screen_path, attachment_type=allure.attachment_type.PNG)
            logger.info("页面已截图，截图保存的路径为: %s" % screen_path)
        except ScreenshotException as e:
            logger.error("截图失败 %s" % e)

    @fail_screenshot
    def click(self, locator):
        """
        根据locator点击元素
        :param locator:
        :return:
        """
        logger.info('Click element by %s: %s ......' % (locator[0], locator[1]))
        try:
            element = self.find_element(*locator)
            element.click()
        except ElementNotVisibleException as e:
            logger.error("无法点击元素: %s" % e)
            raise

    @fail_screenshot
    def clear(self, locator):
        """输入文本框清空操作"""
        logger.info('Clear the input %s: %s ......' % (locator[0], locator[1]))
        try:
            element = self.find_element(*locator)
            element.clear()
            logger.info('清空文本框 ......')
        except Exception as e:
            logger.error("Failed to clear in input box with %s" % e)
            raise

    @fail_screenshot
    def send_keys(self, locator, text):
        """
        文本框输入内容
        :param locator:
        :param text:
        :return:
        """
        logger.info('Input element by %s: %s, value: %s ......' % (locator[0], locator[1], text))
        try:
            element = self.find_element(*locator)
            element.send_keys(text)
        except Exception as e:
            logger.error("Failed to type in input box with %s" % e)
            raise

    @fail_screenshot
    def move_to_element(self, locator):
        """
        鼠标悬停操作
        Usage:
        element = ("id","xxx")
        driver.move_to_element(element)
        """
        logger.info('Move the mouse to the locator %s: %s' % (locator[0], locator[1]))
        try:
            element = self.find_element(*locator)
            ActionChains(self.driver).move_to_element(element).perform()
        except Exception as e:
            logger.error('Move the mouse to the locator appear error {}'.format(e))
            raise

    @fail_screenshot
    def drag_loc_from_to(self, source, target):
        """
        At source WebElement hold the left mouse drag to the target WebElement then release
        :param source:
        :param target:
        :return:
        """
        logger.info('Click the %s and then move to $s' % (source, target))
        try:
            ele_source = self.find_element(*source)
            ele_target = self.find_element(*target)
            ActionChains(self.driver).drag_and_drop(ele_source, ele_target).perform()
        except Exception as e:
            logger.error('Click the and then move element error: {}'.format(e))
            raise

    def back(self):
        """
        浏览器返回窗口
        """
        logger.info('返回上一个页面')
        self.driver.back()

    def forward(self):
        """
        浏览器前进下一个窗口
        """
        logger.info('前进到下一个页面')
        self.driver.forward()

    @staticmethod
    def sleep(seconds=2):
        time.sleep(seconds)
        logger.info("等待 %d 秒" % seconds)

    def close(self):
        """
        关闭浏览器
        """
        try:
            self.driver.close()
            logger.info('关闭浏览器窗口')
        except Exception as e:
            logger.error("关闭浏览器窗口失败 %s" % e)

    def quit(self):
        """
        退出浏览器
        """
        self.driver.quit()

    def get_current_url(self):
        """获取当前页面的url"""
        return self.driver.current_url

    @fail_screenshot
    def get_text(self, locator):
        """获取文本"""
        try:
            element = self.find_element(*locator)
            return element.text
        except AttributeError as e:
            logger.error(e)
            self.get_screen_img()
            raise

    @fail_screenshot
    def get_attribute(self, locator, attribute_name):
        """获取属性"""
        try:
            element = self.find_element(*locator)
            return element.get_attribute(attribute_name)
        except AttributeError as e:
            logger.error(e)
            self.get_screen_img()
            raise

    def js_execute(self, js):
        """执行js"""
        try:
            self.driver.execute_script(js)
        except JavascriptException as e:
            logger.error('Execute js error: {}'.format(e))

    @fail_screenshot
    def js_focus_element(self, locator):
        """聚焦元素"""
        try:
            target = self.find_element(*locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", target)
        except Exception as e:
            logger.error('Focus element error: {}'.format(e))

    def js_scroll_top(self):
        """滚动到顶部"""
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self):
        """滚动到底部(只能滚动body的滚动条)"""
        js = "window.scrollTo(0,document.body.scrollHeight)"
        self.driver.execute_script(js)

    @fail_screenshot
    def select_by_index(self, locator, index):
        """通过索引,index是索引第几个，从0开始"""
        try:
            element = self.find_element(*locator)
            Select(element).select_by_index(index)
        except Exception as e:
            logger.info(e)
            self.get_screen_img()
            raise

    @fail_screenshot
    def select_by_value(self, locator, value):
        """下拉框通过value属性选择"""
        try:
            element = self.find_element(*locator)
            Select(element).select_by_value(value)
        except Exception as e:
            logger.info(e)
            self.get_screen_img()
            raise e

    @fail_screenshot
    def select_by_text(self, locator, choice_text):
        """下拉框通过文本值定位"""
        try:
            element = self.find_element(*locator)
            Select(element).select_by_value(choice_text)
        except Exception as e:
            logger.error(e)
            self.get_screen_img()
            raise

    @fail_screenshot
    def is_text_in_element(self, locator, text, timeout=10):
        """判断文本在元素里，没定位到元素返回False，定位到元素返回判断结果布尔值"""
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(
                EC.text_to_be_present_in_element(locator, text))
            return result
        except TimeoutException:
            logger.info("元素没有定位到:" + str(locator))
            return False

    @fail_screenshot
    def is_text_in_value(self, locator, value, timeout=10):
        """
        判断元素的value值，没定位到元素返回false,定位到返回判断结果布尔值
        result = driver.text_in_element(element, text)
        """
        try:
            result = WebDriverWait(self.driver, timeout, 0.5).until(
                EC.text_to_be_present_in_element_value(locator, value))
            return result
        except TimeoutException:
            logger.info("元素没定位到：" + str(locator))
            return False

    @fail_screenshot
    def is_title(self, title, timeout=10):
        """判断title完全等于"""
        result = WebDriverWait(self.driver, timeout, 0.5).until(EC.title_is(title))
        return result

    @fail_screenshot
    def is_title_contains(self, title, timeout=10):
        """判断title包含"""
        result = WebDriverWait(self.driver, timeout, 0.5).until(EC.title_contains(title))
        return result

    @fail_screenshot
    def is_selected(self, locator, timeout=10):
        """判断元素被选中，返回布尔值"""
        result = WebDriverWait(self.driver, timeout, 0.5).until(
            EC.element_located_to_be_selected(locator))
        return result

    @fail_screenshot
    def is_selected_be(self, locator, selected=True, timeout=10):
        """判断元素的状态，selected是期望的参数true/False
        返回布尔值"""
        result = WebDriverWait(self.driver, timeout, 0.5).until(
            EC.element_located_selection_state_to_be(locator, selected))
        return result

    def is_alert_present(self, timeout=10):
        """判断页面是否有alert，
        有返回alert(注意这里是返回alert,不是True)
        没有返回False"""
        result = WebDriverWait(self.driver, timeout, 0.5).until(EC.alert_is_present())
        return result

    def alert_accept(self):
        """接受alert"""
        try:
            alert = self.driver.switch_to.window()
            logger.info('alert test is %s' % alert.text)
            alert.accept()
        except UnexpectedAlertPresentException as e:
            logger.error('Alert accept error: {}'.format(e))
        except NoAlertPresentException as e1:
            logger.error('Alert accept error: {}'.format(e1))

    @fail_screenshot
    def is_visibility(self, locator, timeout=10):
        """元素可见返回本身，不可见返回False"""
        try:
            result = WebDriverWait(self.driver, timeout, 0.5).until(EC.visibility_of_element_located(locator))
            return result
        except TimeoutException as e:
            logger.info(e)
            return False

    @fail_screenshot
    def is_invisibility(self, locator, timeout=10):
        """元素可见返回False，不可见返回True，没找到元素也返回True"""
        result = WebDriverWait(self.driver, timeout, 0.5).until(
            EC.invisibility_of_element_located(locator))
        return result

    def is_clickable(self, locator, timeout=10):
        """元素可以点击is_enabled返回元素本身，不可点击返回False"""
        result = WebDriverWait(self.driver, timeout, 0.5).until(EC.element_to_be_clickable(locator))
        return result

    def is_located(self, locator, timeout=10):
        """判断元素有没被定位到（并不意味着可见），定位到返回element,没定位到返回False"""
        result = WebDriverWait(self.driver, timeout, 0.5).until(
            EC.presence_of_element_located(locator))
        return result

    def set_element_wait(self, wait_time, locator):
        WebDriverWait(self.driver, wait_time, 0.5).until(EC.presence_of_element_located(locator))

    def upload_file(self, locator, file_path):
        """input 上传文件"""
        try:
            self.find_element(*locator).send_keys(file_path)
            self.sleep(2)
        except Exception as e:
            logger.error("Failed to upload file %s" % e)
            self.get_screen_img()

    def switch_handle(self, title_name):
        """根据窗口title切换窗口"""
        all_handles = self.driver.window_handles()
        for handle in all_handles:
            if self.driver.title.find(title_name) == -1:
                self.driver.switch_to_window(handle)
            else:
                print("Can't find the handle")

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
            return True
        except NoSuchElementException as e:
            logger.error("Element is not present. %s" % e)
            return False

    def close_alert_and_get_its_text(self):
        """close the alter and return its text"""
        try:
            alert = self.driver.switch_to.alert()
            alert_text = alert.text
            logger.info('Close the alert %s ......' % alert_text)
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def get_attribute_text(self, locator):
        try:
            text_content = self.find_element(*locator).get_attribute('textContent')
        except Exception as e:
            logger.error("Failed to upload file %s" % e)
            text_content = ''
            self.get_screen_img()
        return text_content

    def get_screenshot(self, case_name):
        """screen shot"""
        file_name = case_name
        file_path = os.path.join(root_path, 'screenshots', file_name + '.png')
        self.driver.get_screenshot_as_file(file_path)
        allure.attach.file(file_path, attachment_type=allure.attachment_type.PNG)
        logger.info("Screen shot had been saved: %s" % file_path)
        return file_path

    @staticmethod
    def get_current_time():
        temp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        return temp

    @staticmethod
    def get_current_data():
        return time.strftime("%Y-%m-%d", time.localtime())

    def verify_true(self, expr, msg=None):
        try:
            self.case.assertTrue(expr, msg)
        except Exception as e:
            self.get_screen_img()
            raise e

    def verify_in(self, member, container, msg=None):
        try:
            self.case.assertIn(member, container, msg)
        except Exception as e:
            self.get_screen_img()
            raise e
