
# Create your models here.

from logic.DBlogic import *


class BaseTable(models.Model):

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'BaseTable'

class ConfigInfo(BaseTable):
    class Meta:
        verbose_name = '项目配置'
        db_table = 'ConfigInfo'
    status=models.CharField('状态配置',max_length=50)

class ProjectInfo(BaseTable):
    class Meta:
        verbose_name = '项目信息'
        db_table = 'ProjectInfo'

    project_name = models.CharField('项目名称',max_length=50)
    responsible_name = models.CharField('负责人', max_length=20)
    test_user = models.CharField('测试人员', max_length=100)
    dev_user = models.CharField('开发人员', max_length=100)
    publish_app = models.CharField('相关应用', max_length=60)
    simple_desc = models.CharField('简要描述', max_length=500)
    other_desc = models.CharField('其他信息', max_length=100, null=True)
    status = models.IntegerField('有效/无效', default=1)
    objects = ProjectInfoManager()

    def __str__(self):
        return self.project_name

class ModelsInfo(BaseTable):

    class Meta:
        verbose_name = '模块信息'
        db_table = 'ModelsInfo'

    models_name=models.CharField('模块名称',max_length=50)
    models_desc = models.CharField('模块概述',max_length=500)
    status = models.ForeignKey(ConfigInfo,on_delete=models.CASCADE)
    other_desc = models.CharField('其他信息', max_length=100, null=True)
    belong_project=models.ForeignKey(ProjectInfo,on_delete=models.CASCADE,)
    objects = ModuleInfoManager()

    def __str__(self):
        return self.models_name


class CaseInfo(BaseTable):
    class Meta:
        verbose_name = '用例信息'
        db_table = 'CaseInfo'

    type = models.IntegerField('test/config', default=1)
    name = models.CharField('用例/配置名称', max_length=50)
    belong_project = models.CharField('所属项目', max_length=50)
    belong_module = models.ForeignKey(ModelsInfo, on_delete=models.CASCADE)
    include = models.CharField('包含config/test', max_length=200, null=True)
    author = models.CharField('编写人员', max_length=20)
    request = models.TextField('请求信息')
    status = models.IntegerField('有效/无效', default=1)
    objects = TestCaseInfoManager()

    def __str__(self):
        return self.name




