# -*- coding: utf-8 -*-
# @Time          : 2018/4/12 17:20
# @Author        : leo_peng
# @description   : 封装数据库操作
# @File          : DBlogic.py
# @Software      : PyCharm
from django.db import models

'''项目模块操作'''

class ProjectInfoManager(models.Manager):

    def insert_project(self, project_name, responsible_name, test_user, dev_user, publish_app, simple_desc, other_desc):
        '''
        项目模块内容写入
        :param project_name:
        :param responsible_name:
        :param test_user:
        :param dev_user:
        :param publish_app:
        :param simple_desc:
        :param other_desc:
        :return:
        '''
        self.create(project_name=project_name, responsible_name=responsible_name, test_user=test_user, dev_user=dev_user
                    , publish_app=publish_app, simple_desc=simple_desc, other_desc=other_desc)

    def update_project(self, id, project_name, responsible_name, test_user, dev_user, publish_app, simple_desc, other_desc):
        '''
        项目模块内容更新
        :param id:
        :param project_name:
        :param responsible_name:
        :param test_user:
        :param dev_user:
        :param publish_app:
        :param simple_desc:
        :param other_desc:
        :return:
        '''
        obj = self.get(id=int(id))
        obj.projecct_name = project_name
        obj.responsible_name = responsible_name
        obj.test_user = test_user
        obj.dev_user = dev_user
        obj.publish_app = publish_app
        obj.simple_desc = simple_desc
        obj.other_desc = other_desc
        obj.save()
        self.filter(id=id).update(project_name=project_name)

    def get_pro_name(self, project_name, type=True, id=None):
        '''
        判断项目是否已存在
        :param project_name:
        :param type:
        :param id:
        :return:
        '''
        print('判断项目是否存在',project_name,type,id)
        if type:
            # 查询项目，返回查询的存在的数量，0为不存在
            return self.filter(project_name__exact=project_name).count()
        else:
            # 通过项目名和项目ID查询，返回项目信息
            if id is not None:
                return self.get(id=int(id)).project_name
            # 项目名已存在时，返回项目名称
            return self.get(project_name__exact=project_name)

    def get_pro_info(self, type=True):
        '''
        获取所有项目名称，当type=Flase时，查询所有
        :param type:
        :return:
        '''
        if type:
            return self.all().values('project_name')
        else:
            return self.all()


'''模块信息表操作'''


class ModuleInfoManager(models.Manager):

    def insert_module(self, module_name, belong_project, models_desc, other_desc,status):
        '''
        模块信息写入
        :param module_name:
        :param belong_project:
        :param models_desc:
        :param other_desc:
        :return:
        '''
        print(module_name, belong_project, models_desc, other_desc,status)
        self.create(models_name=module_name, belong_project_id=belong_project,
                    models_desc=models_desc, other_desc=other_desc,status_id=status)

    def update_module(self, id, module_name, models_desc,belong_project_id, other_desc,status):
        '''
        模块信息更新
        :param id:
        :param module_name:
        :param models_desc:
        :param belong_project:
        :param other_desc:
        :return:
        '''
        obj = self.get(id=int(id))
        obj.module_name = module_name
        obj.belong_project_id = belong_project_id
        obj.models_desc = models_desc
        obj.other_desc = other_desc
        obj.status_id=status
        obj.save()
        self.filter(id=id).update(models_name=module_name)

    def get_module_name(self, module_name, type=True, id=None, project=None):
        '''
        判断模块是否存在
        :param module_name:
        :param type:
        :param id:
        :param project:
        :return:
        '''
        if type:
            return self.filter(module_name__exact=module_name).count()
        else:
            if id is not None:
                return self.get(id=int(id)).models_name
            return self.get(belong_project__project_name__exact=project, models_name__exact=module_name)

    def get_module_info(self, belong_project):
        '''
        查询项目下的模块，通过创建时间排序显示
        :param belong_project:
        :return:
        '''
        return self.filter(belong_project__project_name__exact=belong_project)\
            .values_list('module_name',flat=True).order_by('-create_time')


'''用例信息表操作'''


class TestCaseInfoManager(models.Manager):

    def insert_case(self,modules,**kwargs):
        '''
        处理前端返回的json，提取字段，插入sql
        :param belong_module:
        :param kwargs:
        :return:
        '''
        case_info = kwargs.get('test').pop('case_info')
        print('插入数据库',kwargs)
        self.create(name=kwargs.get('test').get('name'), belong_project=case_info.pop('belong_project_id'),
                    belong_module_id=modules,author=case_info.pop('author'), include=case_info.pop('include'), request=kwargs)

    def update_case(self, **kwargs):
        '''
        处理前端返回的json，提取字段，更新sql
        :param kwargs:
        :return:
        '''
        case_info = kwargs.get('test').pop('case_info')
        try:
            obj = self.get(id=int(kwargs.get('test').pop('test_index')))
        except:
            obj = self.get(id=int(case_info.pop('test_index')))
        obj.name = kwargs.get('test').get('name')
        obj.author = case_info.pop('author')
        obj.include = case_info.pop('include')
        obj.request = kwargs
        obj.belong_project=case_info.pop('belong_project_id')
        obj.save()


    def insert_config(self, belong_module, **kwargs):
        '''
        处理前端返回项目配置json，提取字段，插入sql
        :param belong_module:
        :param kwargs:
        :return:
        '''
        config_info = kwargs.get('config').pop('config_info')
        self.create(name=kwargs.get('config').get('name'), belong_project=config_info.pop('project'),
                    belong_module=belong_module,
                    author=config_info.pop('config_author'), type=2, request=kwargs)

    def update_config(self, **kwargs):
        '''
        处理前端返回项目配置json，提取字段，更新sql
        :param kwargs:
        :return:
        '''
        config_info = kwargs.get('config').pop('config_info')
        obj = self.get(id=int(config_info.pop('test_index')))
        obj.name = kwargs.get('config').get('name')
        obj.author = config_info.pop('config_author')
        obj.request = kwargs
        obj.save()

    def get_case_name(self, name, module_name, belong_project):
        '''
        通过模块名和项目名统计单个项目的case数量
        :param name:
        :param module_name:
        :param belong_project:
        :return:
        '''
        print('通过模块名和项目名统计单个项目的case数量',name, module_name, belong_project)
        return self.filter(belong_module_id=module_name).filter(name__exact=name).filter(
            belong_project__exact=belong_project).count()

    def get_case_by_id(self, index, type=True):
        '''
        通过id查询case
        :param index:
        :param type:
        :return:
        '''
        if type:
            return self.filter(id=index).all()
        else:
            return self.get(id=index).name
