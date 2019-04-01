__author__ = 'Emerson'
# 专门完成http请求测试的  这是一个测试类
# DDT
import unittest

from ddt import ddt, data
from common.read_config import ReadConfig
from common.http_request import HttpRequest
from common.do_excel import DoExcel
from common.my_log import MyLog
from conf import project_path
from common.do_mysql import DoMysql  # 进行数据库的操作

# 用例的执行模式:
mode = ReadConfig().read_config(project_path.case_conf_path, 'CASE', 'mode')
case_list = eval(ReadConfig().read_config(project_path.case_conf_path, 'CASE', 'case_list'))

# 数据以及ip地址
test_data = DoExcel(project_path.test_data_path, 'test_data').read_data(mode, case_list)
IP = ReadConfig().read_config(project_path.http_conf_path, 'HTTP', 'ip')

COOKIES = None  # 全局变量，初始值

# 日志类
logger = MyLog()


@ddt
class TestHttpRequest(unittest.TestCase):
    def setUp(self):
        self.t = DoExcel(project_path.test_data_path, 'test_data')  # 操作Excel的实例
        # print("开始测试啦")
        logger.info("开始执行测试啦")

    @data(*test_data)
    def test_http_request(self, a):
        # print("测试数据是:",a)
        # print("目前正在执行第%s条用例"%a[0])
        logger.info("测试数据是:{0}".format(a))
        logger.info("目前正在执行第%s条用例" % a[0])
        global COOKIES
        # IP+a[4]  ip地址与uri的拼接
        res = HttpRequest(IP + a[4], a[5]).http_request(a[3], cookies=COOKIES)
        if res.cookies != {}:  # 判断长度或者是判断是否为空{}
            COOKIES = res.cookies  # 只有登录才会产生cookies
        # print(res.json())
        # 检查数据库
        # eval(a[6])
        print(a[7]['sql_data'])
        print(type(a[7]['sql_data']))
        sql_result = DoMysql().do_mysql(a[7]['sql'], (str(a[7]['sql_data']),))
        try:
            self.assertEqual(str(sql_result), a[7]['expected'])
            check_sql_result = 'PASS'
        except AssertionError as e:
            check_sql_result = 'FAIL'
            raise e
        finally:
            self.t.write_data(a[0] + 1, 2, str(sql_result), check_sql_result)

        try:
            self.assertEqual(str(a[6]), res.json()['code'])
            result = 'PASS'
            # self.t.write_data(a[0]+1,str(res.json()),test_result)
        except AssertionError as e:
            result = 'Fail'
            # self.t.write_data(a[0]+1,str(res.json()),test_result)
            raise e  # 跟return一样 中断代码
        finally:  #
            self.t.write_data(a[0] + 1, 1, str(res.json()), result)

    def tearDown(self):
        # print("结束测试了")
        logger.info("结束测试了")
