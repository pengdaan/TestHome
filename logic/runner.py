
# -*- coding: utf-8 -*-
# @Time          : 2018/4/26 12:00
# @Author        : leo_peng
# @description   : 请自行添加描述
# @File          : runner.py
# @Software      : PyCharm
from MITTester.modules import CaseInfo,ModelsInfo,ProjectInfo
from httprunner.cli import *

'''通过test id组装case 供其他方法调用'''


def run_by_single(id):
    testcase_list = []
    obj = CaseInfo.objects.get(id=id, status=1)
    module = obj.belong_module_id
    include = obj.include
    request = obj.request

    # do not have include
    if include == '' or include is None:
        testcase_list.append(eval(request))
        return testcase_list

    else:
        config_test = include.split('>')
        for name in config_test:
            include_request = CaseInfo.objects.get(name__exact=name,
                                                       belong_module=ModelsInfo.objects.get(id=module),
                                                       status=1).request
            testcase_list.append(eval(include_request))
        testcase_list.append(eval(request))
        print('单个用例预运行的数据',testcase_list)
        return testcase_list


'''单个模块组装所有test'''


def run_by_module(id):
    testcase_lists = []
    obj = ModelsInfo.objects.get(id=id, status=1)
    test_index_list = CaseInfo.objects.filter(belong_module=obj, type=1, status=1).values_list('id')
    for index in test_index_list:
        testcase_lists.append(run_by_single(index[0]))
    return testcase_lists


'''运行并返回报告'''


def get_result(test_lists):
    summary = {
        "success": True,
        "stat": {
            'testsRun': 0,
            'successes': 0,
            'failures': 0,
            'errors': 0,
            'skipped': 0,
            'expectedFailures': 0,
            'unexpectedSuccesses': 0
        },
        "platform": {},
        "time": {
            'start_at': '',
            'duration': 0.0,
        },
        "records": [],
    }
    for index in range(len(test_lists)):
        result = main_ate(test_lists[index])

        if index == 0:
            summary["time"]["start_at"] = result["time"].pop("start_at")



'''单个项目组装所有test'''


def run_by_project(id):
    testcase_lists = []
    obj = ProjectInfo.objects.get(id=id, status=1)
    module_index_list = ModelsInfo.objects.filter(belong_project=obj, status=1).values_list('id')
    for index in module_index_list:
        module_id = index[0]
        testcase_lists.extend(run_by_module(module_id))
    return testcase_lists
