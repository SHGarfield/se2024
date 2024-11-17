from django.shortcuts import render

# Create your views here.
# wechat_app/views.py

from django.http import JsonResponse
import requests
import json

def wechat_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        code = data.get('code')
        print(code)
        appid = 'wxb5dbc4b4be36808f'
        secret = 'fff193612d5d2bea5e85689abe27e14a'
        url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'

        response = requests.get(url)
        print(response.text)
        data = response.json()
        print(data)
        if 'openid' in data:
            # 在这里处理登录逻辑，例如创建用户会话或返回用户信息
            return JsonResponse({'status': 'success', 'openid': data['openid']})
        else:
            return JsonResponse({'status': 'fail', 'error': '无法获取用户信息'})
    else:
        return JsonResponse({'status': 'fail', 'error': '仅支持POST请求'})