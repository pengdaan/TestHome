from django.shortcuts import render
import json
from logic.common import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from logic.runner import *
# Create your views here.


# 首页
def index(request):
    return render(request,'index.html')

# 404页面
def page_not_found(request):
    return render_to_response('404.html')

# 500页面
def page_error(request):
    return render_to_response('500.html')


# 项目列表页
def project(request):

    project_list=ProjectInfo.objects.all()
    return render(request,'project.html',{'project_list':project_list})


# 编辑项目
def Editproject(request):

    if request.method=='GET':
        id=request.GET.get('id')
        obj=ProjectInfo.objects.filter(id=id).first()
        return render(request,'edit_project.html',{'obj':obj})
    elif request.is_ajax():
        project_info = json.loads(request.body.decode('utf-8'))
        msg = project_info_logic(type=False, **project_info)
        return HttpResponse(get_ajax_msg(msg, 'true'))


# 添加项目
def add_project(request):

    if request.is_ajax():
        project_info = json.loads(request.body.decode('utf-8'))
        print(project_info)
        msg = project_info_logic(**project_info)
        return HttpResponse(get_ajax_msg(msg, '项目添加成功'))
    elif request.method == 'GET':
        return render(request, 'add_project.html')


# 模块列表
def models(request):
    models_list=ModelsInfo.objects.all()
    project_list=ProjectInfo.objects.all()
    return render(request,'models.html',{'models_list':models_list,'project_list':project_list})


# 添加模块
def add_models(request):

    if request.method=='GET':
        project_list = ProjectInfo.objects.all()
        return render(request, 'add_models.html', {'project_list': project_list})
    elif request.is_ajax():
        models_info = json.loads(request.body.decode('utf-8'))
        print(models_info)
        msg=module_info_logic(**models_info)
        return HttpResponse(get_ajax_msg(msg, 'true'))

# 编辑模块
def edit_models(request):

    if request.method=='GET':
        id=request.GET.get('id')
        obj=ModelsInfo.objects.filter(id=id).first()
        project_list = ProjectInfo.objects.all()
        print(project_list)
        return render(request,'edit_models.html',{'obj':obj,'project_list': project_list})
    elif request.is_ajax():
        project_info = json.loads(request.body.decode('utf-8'))
        msg = module_info_logic(type=False, **project_info)
        return HttpResponse(get_ajax_msg(msg, 'true'))


# 用例列表

def case_list(request):

    case_list=CaseInfo.objects.all()
    return render(request,'case_list.html',{'case_list':case_list})

# 新增用例

def add_case(request):

    project_list=ProjectInfo.objects.all()
    models_list=ModelsInfo.objects.all()
    if request.is_ajax():
        testcase_lists = json.loads(request.body.decode('utf-8'))
        print('添加用例',testcase_lists)
        msg = case_info_logic(**testcase_lists)
        return HttpResponse(get_ajax_msg(msg, '用例添加成功'))
    elif request.method == 'GET':
        return render(request,'add_case.html',{'project_list':project_list,'models_list':models_list})


# 编辑case
def edit_case(request):

    if request.method=='POST':
        id=request.POST.get('id')
        test_info=CaseInfo.objects.get_case_by_id(id)
        try:
            request=eval(test_info[0].request)
            manage_info ={
                'info': test_info[0],
                'request': request['test']
            }
            print(manage_info)
            return render_to_response('edit_case.html',manage_info)
        except:
            testcase_lists = json.loads(request.body.decode('utf-8'))
            msg = case_info_logic(**testcase_lists, type=False)
            return HttpResponse(get_ajax_msg(msg, '用例信息更新成功'))


# 新增配置
def add_config(request):
    '''
    新增接口配置,配置后接口才能正常运行
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, 'add_config.html')
    elif request.is_ajax():
        config_info = json.loads(request.body.decode('utf-8'))
        print(config_info)
        return HttpResponse('test')
    # if request.method=='POST':
    #     id=request.POST.get('id')
    #     test_info=CaseInfo.objects.get_case_by_id(id)
    #     try:
    #         request=eval(test_info[0].request)
    #         manage_info ={
    #             'info': test_info[0],
    #             'request': request['test']
    #         }
    #         print(manage_info)
    #         return render_to_response('edit_case.html',manage_info)
    #     except:
    #         testconfig_lists = json.loads(request.body.decode('utf-8'))
    #         msg = config_info_logic(**testconfig_lists)
    #         return HttpResponse(get_ajax_msg(msg, '用例信息更新成功'))



# 下拉框联动

def filterAppFromSite(request):
    '''
    修改case时，项目和列表下拉联动
    :param request:
    :return:
    '''
    # app_list1 = [{'name': 'project_1', 'value': [{'name': 'models_1'}, {'mame': 'models_2'}]},
    #             {'name': 'project_2', 'value': [{'name': 'models_3'}, {'name': 'models_4'}]}]

    model_list = []
    # 获取所有项目名称
    projects_names = ProjectInfo.objects.values('project_name').all()
    # 遍历项目名称，插入字典，同时通过项目名查询所关联的模块
    for project_name in projects_names:
        projects = str(project_name['project_name'])
        app_dict = {}
        a = []
        belong_project_id = ProjectInfo.objects.values('id').filter(project_name=projects).all()
        for id in belong_project_id:
            id = str(id['id'])
            model = ModelsInfo.objects.values('models_name').filter(belong_project_id=id).all()
            for models in model:
                c = {}
                models= str(models['models_name'])
                c['name'] = models
                a.append(c)
            app_dict['name'] = str(project_name['project_name'])
            app_dict['value'] = a
            model_list.append(app_dict)
    # print(model_list)
    #result=json.dumps(app_list1, ensure_ascii=False)
    result = json.dumps(model_list, ensure_ascii=False)
    return HttpResponse(result)


'''单个执行'''


def run_test(request):


    if request.method == 'POST':
        mode = request.POST.get('mode')
        print(mode)
        id = request.POST.get('id')
        if mode == 'run_by_test':
            result = main_ate(run_by_single(id))
            return render_to_response('report_template.html', result)
        elif mode == 'run_by_module':
            test_lists = run_by_module(id)
            result = get_result(test_lists)
            return render_to_response('report_template.html', result)
        elif mode == 'run_by_project':
            test_lists = run_by_project(id)
            result = get_result(test_lists)
            return render_to_response('report_template.html', result)







import codecs
import simplejson
def mock_test(request):
    response={'status':100,'message':None}
    try:
        path=r'G:\WAPI\restful_api\json\config.json'
        print(path)
        with codecs.open(path, 'r', 'utf-8') as f:
            response = simplejson.loads(f.read())
    except Exception as e:
        response['message'] = str(e)
    result = json.dumps(response, ensure_ascii=False)
    return HttpResponse(result)


def test(request):
    return render(request,'test.html')




