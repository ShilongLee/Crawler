import unittest
import argparse
from importlib import import_module

MODULES = ['douyin', 'bilibili', 'jd', 'kuaishou', 'taobao', 'weibo', 'xhs']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test program.')
    parser.add_argument('-m', '--modules', type=str, help='Modules to test like douyin, detault value to test all modules', default='')
    args = parser.parse_args()

    if args.modules:
        modules = args.modules.split(' ')
    else:
        modules = MODULES

    suite = unittest.TestSuite()
    for module in modules:
        m = import_module(module)
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(getattr(m, 'TestModule')))

    # 运行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
