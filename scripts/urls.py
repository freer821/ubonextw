"""shopexpress URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from user.views import *
from package.views import *

urlpatterns = [
    path('', user_login),
    # user app
    path('login', user_login),
    path('logout', user_logout),
    path('dashboard', user_dashboard),
    path('upload_excel', package_upload),

    path('packages', packagelist),
    path('package_detail', package_detail),
    path('scancode_to_miandan', scancode_to_miandan),
    path('package_action', package_action),

    path('admin/', admin.site.urls)
]
