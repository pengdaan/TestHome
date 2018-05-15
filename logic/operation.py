from django.core.exceptions import ValidationError
from django.db import DataError

from MITTester.models import *


'''项目数据落地'''


def add_project_data(type, **kwargs):
    project_opt = ProjectInfo.objects
    try:
        if type:
            if project_opt.get_pro_name(kwargs.get('project_name')) < 1:
                project_opt.insert_project(kwargs.pop('project_name'), kwargs.pop('responsible_name'),
                                           kwargs.pop('test_user'), kwargs.pop('dev_user'), kwargs.pop('publish_app'),
                                           kwargs.pop('simple_desc'), kwargs.pop('other_desc'))
            else:
                return '该项目已存在，请重新编辑'
        else:
            if kwargs.get('project_name') != project_opt.get_pro_name('', type=False, id=kwargs.get(
                    'index')) and project_opt.get_pro_name(kwargs.get('project_name')) > 0:
                return '该项目已存在， 请重新命名'
            project_opt.update_project(kwargs.pop('index'), kwargs.pop('project_name'), kwargs.pop('responsible_name'),
                                       kwargs.pop('test_user'), kwargs.pop('dev_user'), kwargs.pop('publish_app'),
                                       kwargs.pop('simple_desc'), kwargs.pop('other_desc'))

    except DataError:
        return '字段长度超长，请重新编辑'
    return 'ok'


'''模块数据落地'''


def add_module_data(type, **kwargs):
    module_opt = ModelsInfo.objects
    print(kwargs)
    belong_project = kwargs.pop('belong_project_id')
    status= kwargs.pop('status')
    try:
        if type:
            if module_opt.filter(belong_project_id__exact=belong_project) \
                    .filter(models_name__exact=kwargs.get('models_name')).count() < 1:
                module_opt.insert_module(module_name=kwargs.pop('models_name'), models_desc=kwargs.pop('models_desc'),
                                         status=status,other_desc=kwargs.pop('other_desc'),belong_project=belong_project)
            else:
                return '该模块已在项目中存在，请重新编辑'
        else:
            print('models_name:',kwargs.get('models_name'))
            print('index:',module_opt.get_module_name('', type=False, id=kwargs.get('index')))
            print('是否存在数目:',module_opt.filter(belong_project_id__exact=belong_project).filter(models_name__exact=kwargs.get('models_name')).count() )
            if kwargs.get('models_name') == module_opt.get_module_name('', type=False, id=kwargs.get('index')) \
                    and module_opt.filter(belong_project_id__exact=belong_project) \
                            .filter(models_name__exact=kwargs.get('models_name')).count() > 0:
                return '该模块已存在，请重新命名'
            module_opt.update_module(id=kwargs.pop('index'), module_name=kwargs.pop('models_name'), models_desc=kwargs.get('models_desc'),
                                     belong_project_id=belong_project,
                                     status=status, other_desc=kwargs.pop('other_desc'))
    except DataError:
        return '字段长度超长，请重新编辑'
    return 'ok'


'''用例数据落地'''


def add_case_data(type, **kwargs):
    case_info = kwargs.get('test').get('case_info')
    case_opt = CaseInfo.objects
    name = kwargs.get('test').get('name')
    module = case_info.get('module')
    project = case_info.get('project')
    try:
        if type:
            if case_opt.get_case_name(name, module, project) < 1:
                # belong_module = ModelsInfo.objects.get_module_name(module, type=False, project=project)
                case_opt.insert_case(**kwargs)
            else:
                return '用例或配置已存在，请重新编辑'
        else:
            print(kwargs,'kkkk')
            index = int(kwargs.get('test').get('test_index'))
            #index = int(case_info.get('test').get('test_index'))
            if name != case_opt.get_case_by_id(index, type=False) \
                    and case_opt.get_case_name(name, module, project) > 0:
                return '用例或配置已在该模块中存在，请重新命名'
            else:
                case_opt.update_case(**kwargs)

    except DataError:
        return '字段长度超长，请重新编辑'
    return 'ok'


'''配置数据落地'''


def add_config_data(type, **kwargs):
    case_opt = CaseInfo.objects
    config_info = kwargs.get('config').get('config_info')
    name = kwargs.get('config').get('name')
    module = config_info.get('config_module')
    project = config_info.get('project')
    try:
        if type:
            if case_opt.get_case_name(name, module, project) < 1:
                belong_module = ModelsInfo.objects.get_module_name(module, type=False, project=project)
                case_opt.insert_config(belong_module, **kwargs)
            else:
                return '用例或配置已存在，请重新编辑'
        else:
            index = int(config_info.get('test_index'))
            if name != case_opt.get_case_by_id(index, type=False) \
                    and case_opt.get_case_name(name, module, project) > 0:
                return '用例或配置已在该模块中存在，请重新命名'
            else:
                case_opt.update_config(**kwargs)
    except DataError:
        return '字段长度超长，请重新编辑'
    return 'ok'


'''改变状态'''

def change_status(Model, **kwargs):
    name = kwargs.pop('name')
    obj = Model.objects.get(id=name)
    obj.status = kwargs.pop('status')
    obj.save()
    return 'ok'

