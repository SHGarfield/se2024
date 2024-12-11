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
        print(code)
        appid = 'wxb5dbc4b4be36808f'
        secret = 'fff193612d5d2bea5e85689abe27e14a'
        url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'
        
        #从微信服务器得到含openid的response
        response = requests.get(url)
        response_data=json.loads(response.text)
        print("response_data: ",response_data)
        #将openid存入数据库
        if(ifUserOpenIdExist(response_data['openid']) == True):
            print(f"openid:{response_data['openid']}(已存在)")
        else:
            print(f"openid:{response_data['openid']}(不存在)")
            add_user_to_db(response_data,data)
        if 'openid' in response_data:
            # 在这里处理登录逻辑，例如创建用户会话或返回用户信息
            return JsonResponse({'status': 'success', 'openid': response_data['openid']})
        else:
            return JsonResponse({'status': 'fail', 'error': '无法获取用户信息'})
    else:
        return JsonResponse({'status': 'fail', 'error': '仅支持POST请求'})
    
def ifUserOpenIdExist(_openid):
    return models.UserInfo.objects.filter(openid=_openid).exists()

def add_user_to_db(response_data,data):
    # openid = response_data['openid']
    # username = data.get('nickname')
    # email, gender= "未填写", "未填写"
    # if 'email' in response_data:
    #     email = response_data['email']
    # if 'gender' in response_data:
    #     gender = response_data['gender']
    new_instance = models.UserInfo()
    new_instance.openid = response_data['openid']
    new_instance.username = data.get('nickname')
    new_instance.email = "未填写"
    new_instance.gender= "未填写"
    new_instance.save()
    print(models.UserInfo.objects.all().first())
    
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
import os

UPLOAD_DIR = os.path.join(os.getcwd(), 'avatars')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# @csrf_exempt  # 如果在开发阶段跳过 CSRF 验证
def upload_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        avatar = request.FILES['avatar']  # 获取上传的头像文件
        file_path = os.path.join(UPLOAD_DIR, avatar.name)
        
        # 保存文件
        with open(file_path, 'wb+') as destination:
            for chunk in avatar.chunks():
                destination.write(chunk)
        
        return JsonResponse({"code": 200, "message": "头像上传成功", "file_path": file_path})
    return JsonResponse({"code": 400, "message": "请求无效"}, status=400)
