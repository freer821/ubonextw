from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth.decorators import login_required
import json
from .apps import *
# Create your views here.

@login_required
def package_upload(request):
    try:
        if request.method == 'POST':
            jsonbody = json.loads(request.body)
            response = upload_handle(jsonbody)
            return JsonResponse(response)
        else:
            return render(request, 'uploadpackageexcel.html')
    except Exception as e:
        getLogger().error(e)
        return JsonResponse(getresponsemsg(500,'system error'))



@login_required
def packagelist(request):
    try:
        offset = request.GET.get('offset', '')

        if offset:
            limit = request.GET.get('limit', '10')
            packages = packagelist_handle(int(offset), int(limit))
            return JsonResponse(packages)
        else:
            return render(request, 'packagelist.html')

    except Exception as e:
        getLogger().error('packagelist'+ str(e))
        return HttpResponseRedirect('/')


@login_required
def package_detail(request):
    try:
        pid = request.GET.get('pid', '')
        package = getPackageByID(pid)
        return render(request, 'package-detail.html', {'package': package})

    except Exception as e:
        getLogger().error('package_detail'+ str(e))
        return HttpResponseRedirect('/')


@login_required
def package_action(request):
    try:
        action = request.GET.get('action', '')

        if action == 'pdf':

            return JsonResponse(packages)
        else:
            return JsonResponse(getresponsemsg(400, 'no found action'))

    except Exception as e:
        getLogger().error('package_action'+ str(e))
        return JsonResponse(getresponsemsg(500, str(e)))
