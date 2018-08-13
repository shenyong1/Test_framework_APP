# -*- coding:utf-8 -*-

import unittest,time
from page.page import Page

class DingDang_Login(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = Page()
    @classmethod
    def tearDownClass(cls):
        cls.page.quit()
    @unittest.skip
    def test_a_login(self):
        self.page.username()
        self.page.password()
        self.page.login()
        self.assertTrue(self.page.login_check(self.test_a_login.__name__),'msg')

    def test_b_checkin(self):
        self.page.fangtai()
        time.sleep(3)
        self.page.room()
        time.sleep(1)
        self.page.name()
        self.page.CardID()
        self.page.phone()
        self.page.checkin()
        self.page.confirm()