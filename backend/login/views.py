from django.shortcuts import render

# Create your views here.
# wechat_app/views.py

from django.http import JsonResponse
import requests
import json
from login import models

def wechat_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        code = data.get('code')
        nickname = data.get('nickname')
        print(code)
        appid = 'wxb5dbc4b4be36808f'
        secret = 'fff193612d5d2bea5e85689abe27e14a'
        url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'
        #从微信服务器得到含openid的response
        response = requests.get(url)
        response_data=json.loads(response.text)
        print("response_data: ",response_data)
        #将openid存入数据库
        if(search_db(response_data['openid']) == True):
            print(f"openid:{response_data['openid']}(已存在)")
        else:
            print(f"openid:{response_data['openid']}(不存在)")
            add_user_to_db(response_data)
        if 'openid' in response_data:
            # 在这里处理登录逻辑，例如创建用户会话或返回用户信息
            return JsonResponse({'status': 'success', 'openid': response_data['openid']})
        else:
            return JsonResponse({'status': 'fail', 'error': '无法获取用户信息'})
    else:
        return JsonResponse({'status': 'fail', 'error': '仅支持POST请求'})
    
def search_db(_openid):
    return models.UserInfo.objects.filter(openid=_openid).exists()

def add_user_to_db(response_data):
    openid = response_data['openid']
    username = response_data['username']
    email, gender= "未填写", 0
    if 'email' in response_data:
        email = response_data['email']
    if 'gender' in response_data:
        gender = response_data['gender']
    models.UserInfo.objects.create(openid, username,email,gender)