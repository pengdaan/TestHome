"""TestHmoe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from MITTester.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',index,name='index'),
    url(r'^index.html',index,name='index'),
    url(r'^project/',project),
    url(r'^add_project.html',add_project),
    url(r'^api/add_project/',add_project),
    url(r'^edit_project.html$', Editproject),
    url(r'^models.html',models),
    url(r'^add_models.html',add_models),
    url(r'^api/add_model/',add_models),
    url(r'^edit_models.html$', edit_models),
    url(r'^case_list.html',case_list),
    url(r'^add_case.html$',add_case),
    url(r'^api/add_case/',add_case),
    url(r'^api/run_case/',run_test),
    url(r'^edit_case.html$', edit_case),
    url(r'^api/edit_case/', edit_case),
    url(r'^404/', page_not_found),
    url(r'^500/', page_error),
    url(r'^test/',mock_test)
]
