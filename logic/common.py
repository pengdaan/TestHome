# -*- coding: utf-8 -*-
# @Time          : 2018/4/13 14:47
# @Author        : leo_peng
# @description   : 请自行添加描述
# @File          : common.py
# @Software      : PyCharm
from logic.operation import *


'''项目信息逻辑判断'''


def project_info_logic(type=True, **kwargs):
    if kwargs.get('project_name') is '':
        return '项目名称不能为空'
    if kwargs.get('responsible_name') is '':
        return '负责人不能为空'
    if kwargs.get('test_user') is '':
        return '测试人员不能为空'
    if kwargs.get('dev_user') is '':
        return '开发人员不能为空'
    if kwargs.get('publish_app') is '':
        return '发布应用不能为空'

    return add_project_data(type, **kwargs)


'''模块信息逻辑判断'''


def module_info_logic(type=True, **kwargs):
    if kwargs.get('models_name') is '':
        return '模块名称不能为空'
    if kwargs.get('belong_project_id') is '':
        return '请先添加项目'
    if kwargs.get('status') is '':
        return '模块状态不能为空'
    return add_module_data(type, **kwargs)


'''前端test信息转字典'''


def key_value_dict(**kwargs):
    if not kwargs:
        return None
    # 对以列表返回可遍历的(键, 值) 元组数组排序
    sorted_kwargs = sorted(kwargs.items())
    # print('sorted_kwargs',sorted_kwargs)
    # 清空字典
    kwargs.clear()
    # 取整除 - 返回商的整数部分
    half_index = len(sorted_kwargs) // 2
    # 遍历列表元组，返回{key:value}
    for value in range(half_index):
        key = sorted_kwargs[value][1]
        value = sorted_kwargs[half_index + value][1]
        if key != '' and value != '':
            kwargs.setdefault(key, value)
    print('key_value_dict_data:',kwargs)
    return kwargs


'''前端test信息转列表'''


def key_value_list(name='false', **kwargs):
    if not kwargs:
        return None
    # 对以列表返回可遍历的(键, 值) 元组数组排序
    sorted_kwargs = sorted(kwargs.items())
    # print('sorted_kwargs',sorted_kwargs)
    lists = []
    if name == 'true':
        half_index = len(sorted_kwargs) // 3
        for value in range(half_index):
            check = sorted_kwargs[value][1]
            expected = sorted_kwargs[value + half_index][1]
            comparator = sorted_kwargs[value + 2 * half_index][1]
            if check != '' and expected != '':
                lists.append({'check': check, 'comparator': comparator, 'expected': expected})
    else:
        half_index = len(sorted_kwargs) // 2

        for value in range(half_index):
            key = sorted_kwargs[value][1]
            value = sorted_kwargs[half_index + value][1]
            if key != '' and value != '':
                lists.append({key: value})
    if not lists:
        return None
    # print('key_value_list_data:',lists)
    return lists


'''用例信息逻辑判断'''


def case_info_logic(type=True, **kwargs):
    test = kwargs.pop('test')
    if test.get('name').get('case_name') is '':
        return '用例名称不可为空'
    if test.get('name').get('belong_project_id') is None or test.get('name').get('belong_project_id') is '':
        return '请先添加项目'
    if test.get('name').get('models_name') is None or test.get('name').get('models_name') is '':
        return '请先添加模块'
    if test.get('name').get('author') is '':
        return '创建者不能为空'
    if test.get('request').get('url') is '':
        return '接口地址不能为空'
    if not test.get('validate'):
        return '至少需要一个结果校验！'
    name = test.pop('name')
    test.setdefault('name', name.pop('case_name'))
    test.setdefault('case_info', name)
    validate = test.pop('validate')
    # 字典 setdefault() 函数和get() 方法类似, 如果键不存在于字典中，将会添加键并将值设为默认值。
    test.setdefault('validate', key_value_list(name='true', **validate))
    extract = test.pop('extract')
    if extract:
        test.setdefault('extract', key_value_list(**extract))
    request_data = test.get('request').pop('request_data')
    date_type = test.get('request').pop('type')
    if request_data and date_type:
        test.get('request').setdefault(date_type, key_value_dict(**request_data))
    headers = test.get('request').pop('headers')
    if headers:
        test.get('request').setdefault('headers', key_value_dict(**headers))
    variables = test.pop('variables')
    if variables:
        test.setdefault('variables', key_value_list(**variables))
    setup = test.pop('setup')
    if setup:
        test.setdefault('setup', key_value_list(**setup))
    teardown = test.pop('teardown')
    if teardown:
        test.setdefault('teardown', key_value_list(**teardown))
    kwargs.setdefault('test', test)
    print('case_info_logic_data:',kwargs)
    return add_case_data(type, **kwargs)



'''ajax异步提示'''


def get_ajax_msg(msg, success):
    if msg is 'ok':
        return success
    else:
        return msg