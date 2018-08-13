# -*- coding:utf-8 -*-

from lib.appController import AppContoller,device_name_queue
from appCase.test_login import DingDang_Login
from lib.log import logger
from lib.result import Result
from lib import HTMLTestAppRunner
from conf.path import APPREPORT_PATH
import threading,unittest

local = threading.local()


class App(object):
    def __init__(self):
        self.c = AppContoller()

    def case(self):
        #通过导入测试类来实现生成测试集
        suite = unittest.TestLoader().loadTestsFromTestCase(DingDang_Login)
        #生成一个空的结果集
        local.result = Result()

        #运行case,并更新结果，记录通过与失败的case
        res = suite.run(local.result)

        #将结果通过测试手机名称进行区分
        logger.debug('当前线程的的名字：%s' % threading.current_thread().getName())
        # 当前线程的名字 就是当前运行手机的名字
        result = {threading.current_thread().getName(): res}

        for deviceName,result in result.items():
            html = HTMLTestAppRunner.HTMLTestRunner(stream=open(APPREPORT_PATH.format('{}.html'.format(deviceName)),'wb'),
                                                    verbosity=2,
                                                    title='测试报告')

            #这个方法就是生成报告的主要函数
            html.generateReport('',result)

    def run(self):
        threads = []
        self.c.server()
        if self.c.test_server():
            drivers = self.c.driver()
            logger.info('开始执行CASE！当前启动【%s】个DRIVER！' % drivers.qsize())
            # 根据由多少个driver执行多少次case
            for case in range(drivers.qsize()):
                #根据driver启动多线程路case,对每个线程通过手机名称命名
                t = threading.Thread(target=self.case,name=device_name_queue.get())
                threads.append(t)
                t.start()
            for i in threads:
                i.join()


if __name__ == '__main__':
    App().run()