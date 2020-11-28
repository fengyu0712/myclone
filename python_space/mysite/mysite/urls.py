"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from learn import views as learn_views
from django.conf.urls import url,include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     re_path('home/', learn_views.index, name='home'),
#     re_path('add/', learn_views.add,name='add'),
#     re_path(r'^add2/(\d+)/(\d+)/$', learn_views.add2, name='add2'), # 2. 采用 /add/3/4/ 这样的网址的方式
# ]

#覆盖用户旧版的网址跳转
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',learn_views.home2, name='home'),
    # url('admin/', admin.site.urls),
    re_path('add/', learn_views.add,name='add'),
    url(r'^add2/(\d+)/(\d+)/$', learn_views.old_add2_redirect),
    url(r'^new_add/(\d+)/(\d+)/$', learn_views.add2, name='add2'),
    re_path('接口/', learn_views.index,name='接口'),
]
