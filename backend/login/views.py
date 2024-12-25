"""
文件描述：用于处理微信小程序登录的view函数

接口函数：
1、wechat_login(request)：处理微信小程序登录请求
2、upload_username(request)：处理上传（修改）用户名请求

"""

from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
from login import models


def wechat_login(request):
    """
    处理微信小程序登录的POST请求

    获取小程序前端生成的code，发送给微信服务器，接收到微信服务器返回的openid以后，查询数据库中是否由该用户，返回JSON响应。

    Args:
        request (HttpRequest): Django的HTTP请求对象

    Returns:
        JsonResponse: 包含登录状态和用户信息的JSON响应
    """
    if request.method == "POST":
        # 从微信服务器获取openid
        response = getOpenIdFromWechat(request)
        response_data = json.loads(response.text)

        # 如果没有获取到openid，返回错误信息
        if "openid" not in response_data:
            return JsonResponse({"status": "fail", "error": "无法获取用户信息"})

        # 通过openid查询用户是否在数据库中
        if isUserOpenIdExist(response_data["openid"]) == True:
            # 如果存在，则返回username和openid
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
                }
            )
        else:
            # 如果不存在，只返回openid
            return JsonResponse(
                {
                    "status": "success",
                    "openid": response_data["openid"],
                    "isInDatabase": False,
                }
            )
    else:
        # 如果不是POST请求，返回错误信息
        return JsonResponse({"status": "fail", "error": "仅支持POST请求"})


def getOpenIdFromWechat(request):
    """
    将前端生成的code发往微信服务器，从微信服务器获取openid。

    Args:
        request (HttpRequest): Django的HTTP请求对象

    Returns:
        requests.Response: 微信服务器返回的响应对象，包含openid信息
    """
    # 获得数据报
    data = json.loads(request.body)
    # 从主体内容中提取code
    code = data.get("code")
    # 将code和小程序验证信息发送给微信服务器
    appid = "wxb5dbc4b4be36808f"
    secret = "fff193612d5d2bea5e85689abe27e14a"
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code"

    # 从微信服务器得到含openid的response
    return requests.get(url)


def isUserOpenIdExist(_openid):
    """
    检查数据库中是否存在指定openid的用户

    Args:
        _openid (str): 需要检查的openid

    Returns:
        bool: 如果存在返回True，否则返回False
    """
    return models.UserInfo.objects.filter(openid=_openid).exists()


def upload_username(request):
    """
    处理上传（修改）用户名的请求。

    Args:
        request (HttpRequest): Django的HTTP请求对象

    Returns:
        JsonResponse: 包含操作结果的JSON响应
    """
    if request.method == "POST":
        # 获得数据报
        data = json.loads(request.body)
        # 从主体内容中提取openid和昵称
        openid = data.get("openid")
        nickname = data.get("nickname")

        #如果nickname长度大于10，则返回错误信息
        if len(nickname) > 10:
            return JsonResponse(
                {"status": "error", "message": "Username too long"}, status=400
            )

        try:
            if isUserOpenIdExist(openid):
                # 如果用户已经存在，更新用户名
                models.UserInfo.objects.filter(openid=openid).update(username=nickname)
            else:
                # 如果用户不存在，添加用户到数据库
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
    """
    将新用户添加到数据库。

    Args:
        openid (str): 用户的openid
        username (str): 用户的昵称
    """
    new_instance = models.UserInfo()
    new_instance.openid = openid
    new_instance.username = username
    new_instance.save()
