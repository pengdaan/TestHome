from django.shortcuts import render
import json
from logic.common import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from httprunner.cli import *
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
        return HttpResponse(get_ajax_msg(msg, '项目信息更新成功'))


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
        return HttpResponse(get_ajax_msg(msg, '模块添加成功'))

# 编辑项目
def edit_models(request):

    if request.method=='GET':
        id=request.GET.get('id')
        obj=ModelsInfo.objects.filter(id=id).first()
        project_list = ProjectInfo.objects.all()
        return render(request,'edit_models.html',{'obj':obj,'project_list': project_list})
    elif request.is_ajax():
        project_info = json.loads(request.body.decode('utf-8'))
        msg = module_info_logic(type=False, **project_info)
        return HttpResponse(get_ajax_msg(msg, '模块信息更新成功'))


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
        print(testcase_lists)
        msg = case_info_logic(**testcase_lists)
        return HttpResponse(get_ajax_msg(msg, '用例添加成功'))
    elif request.method == 'GET':
        return render(request,'add_case.html',{'project_list':project_list,'models_list':models_list})

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