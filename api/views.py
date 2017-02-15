import json
import requests
from django.shortcuts import HttpResponse

def get_cmdb(application, ipaddress):
    headers = {'Authorization': 'token 354389e68419190e77ecac39a3dd50b2b83714e0'}
    url = 'http://cmdb_v2.ops.ymatou.cn/api/cmdb/applications/applicationgroup.json?application__name={}&ipaddresses={}'.format(application, ipaddress)
    r = requests.get(url, headers=headers)
    data = r.json()
    if data.get('count') == 0:
        return None
    else:
        return data.get('results')[0].get('environment')


def get_env(request):
    try:
        if request.method == 'GET':
            application = request.GET.get("application")
            ipaddress = request.GET.get("ipaddress")
            if not application or not ipaddress:
                return HttpResponse(json.dumps({'code':1, 'content': 'need application and ipaddress'}))
            env = get_cmdb(application, ipaddress)
            if env == 'Production':
                return HttpResponse(json.dumps({'code':0, 'environment': 'PRD'}))
            elif env == 'Staging':
                return HttpResponse(json.dumps({'code':0, 'environment': 'STG'}))
            elif env == None:
                return HttpResponse(json.dumps({'code':0, 'environment': None}))
            else:
                return HttpResponse(json.dumps({'code':1, 'content': 'error environment {}'.format(env)}))
        else:
            return HttpResponse(json.dumps({'code': 1, 'content': 'need get!'}))
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'content': str(e)}))
