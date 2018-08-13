# -*- coding:utf-8 -*-

from lib.appController import driver_queue
from lib.pyapp import Pyapp
from appium.webdriver.common.touch_action import TouchAction
from lib.log import logger
import threading,time

local = threading.local()

#配置在实例化时，去mq中获取创建好的driver

class BasePage(object):
    def __init__(self):
        local.driver = driver_queue.get()
        local.pyapp = Pyapp(local.driver)

    def quit(self):
        local.pyapp.quit()

    def reset_package(self):
        local.pyapp.reset()

class Dingdang_Login_Page(BasePage):
    def username(self):
        css = 'id=>com.sankuai.pms:id/edit_username'
        local.pyapp.type(css,18221293942)
    def password(self):
        css = 'id=>com.sankuai.pms:id/edit_password'
        local.pyapp.type(css,1234567)
    def login(self):
        css = 'id=>com.sankuai.pms:id/btn_login'
        local.pyapp.click(css)

    def login_check(self,name):
        css = 'content=>首页'
        return local.pyapp.wait_and_save_exception(css,name)

class Dingdang_index(Dingdang_Login_Page):
    def fangtai(self):
        css='name=>房态'
        local.pyapp.click(css)

class Fangtai(Dingdang_index):
    def room(self):
        positions = [(256,300)]
        local.pyapp.taps(positions)

    def name(self):
        css='name=>请输入姓名'
        local.pyapp.type(css,'沈勇')
    def CardID(self):
        css='name=>请输入证件号'
        local.pyapp.type(css,'430527199206168115')

    def phone(self):
        css='name=>请输入手机号'
        local.pyapp.type(css,18221293942)

    def checkin(self):
        css='name=>办理入住'
        local.pyapp.click(css)

    def confirm(self):
        css='id=>com.sankuai.pms:id/sure'
        local.pyapp.click(css)



class Page(Fangtai):
    pass