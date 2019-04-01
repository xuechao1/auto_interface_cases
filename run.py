__author__ = 'Emerson'
import unittest
import time
import HTMLTestRunnerNew
import HTMLTestRunner

from common.test_http_request import TestHttpRequest

suite = unittest.TestSuite()
loader = unittest.TestLoader()
suite.addTest(loader.loadTestsFromTestCase(TestHttpRequest))

now = time.strftime('%Y-%m-%d_%H_%M_%S')  # 获取当前时间
file_path = 'test' + now + '.html'

# 执行用例
with open(file_path, 'wb') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=2, title=None, description=None, tester='summer')
    runner.run(suite)
