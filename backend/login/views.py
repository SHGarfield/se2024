from django.shortcuts import render

# Create your views here.
# wechat_app/views.py

from django.http import JsonResponse
import requests
import json
from login import models


def wechat_login(request):
    print("\n---[wechat_login]---")
    if request.method == "POST":
        # 从微信服务器获取openid
        response = getOpenIdFromWechat(request)
        response_data = json.loads(response.text)
        print("response_data: ", response_data)

        if "openid" not in response_data:
            return JsonResponse({"status": "fail", "error": "无法获取用户信息"})

        # 将openid存入数据库
        if isUserOpenIdExist(response_data["openid"]) == True:
            print(f"openid:{response_data['openid']}(已存在)")
            # 到数据库中找到openid对应的用户信息
            userinfo = models.UserInfo.objects.filter(
                openid=response_data["openid"]
            ).first()
            return JsonResponse(
                {
                    "status": "success",
                    "openid": response_data["openid"],
                    "isInDatabase": True,
                    "username": userinfo.username,
                    "avatar_url": userinfo.avatar_url,
                }
            )
        else:
            print(f"openid:{response_data['openid']}(不存在)")
            return JsonResponse(
                {
                    "status": "success",
                    "openid": response_data["openid"],
                    "isInDatabase": False,
                }
            )
    else:
        return JsonResponse({"status": "fail", "error": "仅支持POST请求"})


def getOpenIdFromWechat(request):
    # 获得数据报
    data = json.loads(request.body)
    print("request_body", data)
    # 从主体内容中提取code
    code = data.get("code")
    print("code", code)
    appid = "wxb5dbc4b4be36808f"
    secret = "fff193612d5d2bea5e85689abe27e14a"
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code"

    # 从微信服务器得到含openid的response
    return requests.get(url)


def isUserOpenIdExist(_openid):
    return models.UserInfo.objects.filter(openid=_openid).exists()


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
import os

UPLOAD_DIR = os.path.join(os.getcwd(), "static", "avatar")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# @csrf_exempt  # 如果在开发阶段跳过 CSRF 验证
def upload_avatar(request):
    print("\n---[upload_avatar]---")
    if request.method == "POST" and request.FILES.get("avatar"):
        avatar = request.FILES["avatar"]  # 获取上传的头像文件
        file_path = os.path.join(UPLOAD_DIR, avatar.name)

        # 保存文件
        with open(file_path, "wb+") as destination:
            for chunk in avatar.chunks():
                destination.write(chunk)

        # 接受openid
        openid = request.POST.dict().get("openid", None)
        print("openid:", openid)
        # 将文件路径保存到数据库
        user = models.UserInfo.objects.filter(openid=openid).first()
        user.avatar_url = file_path
        user.save()
        showAllUser()
        return JsonResponse(
            {"code": 200, "message": "头像上传成功", "file_path": file_path}
        )
    return JsonResponse({"code": 400, "message": "请求无效"}, status=400)


def upload_username(request):
    print("\n---[upload_username]---")
    if request.method == "POST":
        # 获得数据报
        data = json.loads(request.body)
        print("request_body", data)
        # 从主体内容中提取code
        openid = data.get("openid")
        nickname = data.get("nickname")
        try:
            add_user_to_db(openid, nickname)
            return JsonResponse(
                {"status": "success", "message": "Username updated successfully"}
            )
        except Exception as e:
            # 其他错误处理
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        # 如果不是POST请求，返回错误信息
        return JsonResponse(
            {"status": "error", "message": "Invalid request method"}, status=405
        )


def add_user_to_db(openid, username):
    new_instance = models.UserInfo()
    new_instance.openid =openid
    new_instance.username = username
    new_instance.email = "未填写"
    new_instance.gender = "未填写"
    new_instance.save()
    
def showAllUser():
    print("\n---[showAllUser]---")
    all_entries = models.UserInfo.objects.all()
    for entry in all_entries:
        print(
            "--user",
            entry.openid,
            entry.username,
            entry.email,
            entry.gender,
            entry.avatar_url,
        )
