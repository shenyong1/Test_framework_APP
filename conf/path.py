import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 报告地址
REPOR_TPATH = os.path.join(BASE_PATH,'report')

LOG_PATH = os.path.join(BASE_PATH,'log')


#用例存放地址
WEBCASE_PATH = os.path.join(BASE_PATH,'test_case')

#报告截图存放地址
APPPICTURE_PATH = os.path.join(REPOR_TPATH,'app_picture','{}/')

#设备配置地址
APP_PATH = os.path.join(BASE_PATH,'conf','appController.yml')

#生成报错截图的地址
APPERROR_PATH = '../report/app_picture/{}/'

APPREPORT_PATH = os.path.join(REPOR_TPATH,'{}')




