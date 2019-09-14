from django.shortcuts import HttpResponseRedirect, render
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
import json
from scripts.utils import *
from django.contrib.auth.decorators import login_required

from package.apps import getPackageCount

# Create your views here.
def user_login(request):
    try:
        if request.method == "POST":
            request_body = json.loads(request.body)
            username = request_body['email']
            password = request_body['password']

            user = authenticate(username=username, password=password)
            if user is None:
                getLogger().info(username + ' auth failed')
                return JsonResponse(getresponsemsg(204, "用户名或密码错误"))
            else:
                getLogger().info(username + ' logged in')
                login(request, user)

            return JsonResponse(getresponsemsg(200, "dashboard"))

        else:
            if request.user.is_authenticated:
                return render(request, 'login.html', {'is_logged': True})
            else:
                return render(request, 'login.html', {})
    except Exception as e:
        getLogger().error('user_login:' + str(e))
        return JsonResponse(getresponsemsg(500, "系统错误，请联系客服"))


def user_logout(request):
    try:
        getLogger().info('user_logout:' + str(request.user))
        logout(request)
        return HttpResponseRedirect('/')
    except Exception as e:
        getLogger().error('user_logout:'+str(e))
        return HttpResponseRedirect('/')


@login_required
def user_dashboard(request):
    try:
        packages_total_count = getPackageCount()
        dashboard_info = {
            'packages_total_count': packages_total_count
        }
        return render(request, 'dashboard.html', {'dashboard_info':dashboard_info})
    except Exception as e:
        getLogger().error(e)
        return HttpResponseRedirect('/')
