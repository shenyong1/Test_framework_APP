# -*- coding:utf-8 -*-
from lib.tool import Tool
from appium import webdriver
from lib.log import logger
from conf.path import LOG_PATH,APPPICTURE_PATH
import os,subprocess,time,queue,threading

#多线程数据隔离
local = threading.local()
#存放driver 的队列
driver_queue = queue.Queue()
#存放手机设备名称队列
device_name_queue = queue.Queue()


class AppContoller(object):
    def __init__(self):
        self.tool = Tool()
        #配置信息
        self.yml = self.tool.app_data
        # 所有手机配置信息
        self.devices = self.yml.get('devices')
        # 测试app的信息
        self.app = self.yml.get('tester')
        # Android OR iOS
        self.device_type = self.yml.get('device_type')
        # 用于校验服务是否成功，存储端口号
        self.ports = []

    def kill_server(self):
        """
        adb如果重启  夜游神将不会被查到
        :return:
        """
        logger.debug('执行[KILL SERVER]操作:%s' % subprocess.getoutput("taskkill /F /IM node.exe /t"))
        # logger.debug('重启ADB服务！%s' % subprocess.getoutput("adb kill-server"))

    def server_command(self,**kwargs):
        command = 'appium -a {ip} -p {port} -U {udid} -g {log}'.format(ip = kwargs.get('ip'),
                                                                       port = kwargs.get('port'),
                                                                       udid = kwargs.get('udid'),
                                                                       log = kwargs.get('log_path'))
        logger.debug('启动服务执行的命令：%s' % command)
        subprocess.Popen(command,stdout=open(kwargs.get('log_path'),'a+'),stderr=subprocess.PIPE,shell=True)

    def server(self):
        #每次启动前，先清掉上次还存活的端口
        self.kill_server()
        threads_server = []
        for device in self.devices.get(self.device_type):
            #将手机操作log加到配置中
            device.update({'log_path':os.path.join(LOG_PATH,'%s.log'%device.get('name'))})
            logger.debug("每个手机的信息：%s" % device)
            # 提取校验服务启动成功的端口
            self.ports.append(device.get('port'))

            # 启动多线程开启服务
            t = threading.Thread(target=self.server_command,kwargs=device)
            threads_server.append(t)
            t.start()

        for i in threads_server:
            i.join()

    def test_server(self):
        while True:
            for port in self.ports:
                #通过查看是否有返回值来确定是否启动
                test_out_put = subprocess.getoutput("netstat -ano | findstr %s" % port)
                #如果有，则从list中删除这个端口，直到list为空，代表启动成功，跳出循环
                if test_out_put:
                    logger.debug('检验服务启动：%s' % test_out_put)
                    self.ports.remove(port)
                else:
                    logger.debug('端口 【%s】 服务启动失败5秒钟后尝试' % port)
            if not self.ports:
                break
            time.sleep(5)
        logger.debug('全部服务启动成功！')
        return True

    def driver_command(self,**kwargs):
        local.desired_caps = {}
        local.desired_caps.update(kwargs)
        # logger.debug('设备信息：%s'%local.desired_caps)
        url = 'http://{ip}:{port}/wd/hub'.format(port = local.desired_caps.get('port'),
                                                 ip = local.desired_caps.get('ip'))
        logger.debug('启动的Url：%s' % url)
        driver = webdriver.Remote(url,local.desired_caps)
        # 通过消息对列传递driver驱动
        driver_queue.put(driver)
        # 存放手机名称的对列(用于后续对线程名进行区分)
        device_name_queue.put(local.desired_caps.get('name'))
        # 创建错误图片存放的路径
        picture = APPPICTURE_PATH.format(local.desired_caps.get('name'))
        # 如果存在则清除目录下的所有内容
        if os.path.exists(picture):
            self.tool.app_clear(picture)
        else:
            # 如果不存在path 则递归创建目录
            os.makedirs(picture)

    def driver(self):
        thread_driver = []
        for device_app in self.devices.get(self.device_type):
            # 将测试的app信息增加到 手机的配置文件中
            device_app.update(self.app)
            #多线程启动
            d = threading.Thread(target=self.driver_command,kwargs=device_app)
            thread_driver.append(d)
            d.start()
        for j in thread_driver:
            j.join()

        # 所有driver启动成功后 返回driver的mq
        # logger.debug('mq:%s'%driver_queue.get())
        return driver_queue




if __name__ == '__main__':
    t = AppContoller()
    t.server()
    # t.test_server()
    # t.driver()