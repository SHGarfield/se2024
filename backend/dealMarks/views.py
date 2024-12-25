from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timezone, timedelta
import requests
import json
from dealMarks import models

# Create your views here.
import sqlite3
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def addMarks(request):
    """
    添加路线到数据库。

    Args:
        request (HttpRequest): Django的HTTP请求对象，预期为POST请求。

    Returns:
        JsonResponse: 操作成功的JSON响应。
    """
    if request.method == "POST":
        #获得请求体中的数据
        databody = json.loads(request.body)

        # 创建一个新的实例并存储JSON数组数据
        new_instance = models.Marks()
        new_instance.openid = databody["openid"]
        new_instance.title = databody["title"]
        new_instance.content = databody["content"]
        new_instance.marks = databody["marks"]
        new_instance.isprivate = databody["isprivate"]

        # 获取当前时间并存储
        current_utc_time = datetime.now(timezone.utc)# 获取当前UTC时间
        beijing_time = current_utc_time + timedelta(hours=8) # 将UTC时间转换为北京时间（UTC+8）
        beijing_time = beijing_time.replace(microsecond=0)# 确保时间只精确到秒
        new_instance.modified_time = beijing_time
        new_instance.save()
    
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "fail", "error": "仅支持POST请求"})


def getMarks(request):
    """
    根据openid和隐私设置获取标记信息。

    Args:
        request (HttpRequest): Django的HTTP请求对象，预期为POST请求。

    Returns:
        JsonResponse: 包含匹配标记信息的JSON响应。
    """
    if request.method == "POST":
        databody = json.loads(request.body)

        # 获取请求体中的openid和isprivate字段
        isprivate = databody.get("isprivate")
        openid = databody.get("openid")
        
        # 过滤出所有符合条件的条目
        if isprivate:
            # 如果isprivate为True，只返回私有的条目(路线草稿)
            matching_entries = models.Marks.objects.filter(
                openid=openid, isprivate=True
            )
        else:
            # 如果isprivate为False，只返回非私有的条目(公开路线)
            matching_entries = models.Marks.objects.filter(
                openid=openid, isprivate=False
            )

        # 将查询集转换为列表
        entries_list = list(
            matching_entries.values("id", "modified_time", "title", "content", "marks")
        ) 
        
        # 将列表作为JSON响应发送到请求端
        return JsonResponse({"data": entries_list}, safe=False)
    
    else:
        return JsonResponse({"status": "fail", "error": "仅支持POST请求"})


@require_http_methods(["GET"])
def getAllMarks(request):
    """
    获取所有非私有的路线。

    Args:
        request (HttpRequest): Django的HTTP请求对象，预期为GET请求。

    Returns:
        JsonResponse: 包含所有非私有标记信息的JSON响应。
    """

    # 过滤出所有符合条件的条目（非私有的）
    matching_entries = models.Marks.objects.filter(isprivate=False)

    # 将查询集转换为列表
    entries_list = list(
        matching_entries.values("id", "modified_time", "title", "content", "marks")
    )
    # 将列表作为JSON响应发送到请求端
    return JsonResponse({"data": entries_list}, safe=False)

@require_http_methods(["PUT"])  # 限制这个视图只接受PUT请求
def setRouteIsPrivate(request):
    """
    设置一条路线的可见范围。
    """
    # 获取请求体中的数据
    data = json.loads(request.body)
    
    # 获取请求体中的openid和isprivate字段
    isprivate = data.get("isprivate")
    openid = data.get("openid")
    routeid=data.get("routeid")
        
    
    # 过滤出所有符合条件的条目
    matching_entries = models.Marks.objects.filter(
            openid=openid, id=routeid
        ).first()
    if matching_entries is None:
        return JsonResponse({
            'status': 'fail',
            'message': '路线不存在',
        })
    #设置matching_entries的isprivate字段
    matching_entries.isprivate=isprivate
    matching_entries.save()
    
    # 响应请求
    return JsonResponse({
        'status': 'success',
        'message': '设置可见范围成功',
        'isprivate': isprivate  # 将接收到的数据回传给客户端
    })
    
@require_http_methods(["PUT"])  # 限制这个视图只接受PUT请求
def deleteRoute(request):
    """
    删除指定路线。
    """
    # 获取请求体中的数据
    data = json.loads(request.body)
    
    # 获取请求体中的openid和isprivate字段
    openid = data.get("openid")
    routeid=data.get("routeid")
        
    
    # 过滤出所有符合条件的条目
    matching_entries = models.Marks.objects.filter(
            openid=openid, id=routeid
        ).first()
    
    #如果没找到匹配的路线（正常情况下不会发生）
    if matching_entries is None:
        return JsonResponse({
            'status': 'fail',
            'message': '路线不存在',
        })
        
    #删除数据库中的matching_entries
    matching_entries.delete()
    
    # 响应请求
    return JsonResponse({
        'status': 'success',
        'message': '删除路线成功',
    })

@require_http_methods(["PUT"])  # 限制这个视图只接受PUT请求
def modifyMarks(request):
    """
    修改指定路线。
    """
    
    #获得请求体中的数据
    databody = json.loads(request.body)

    # 搜索对应路线并更新数据库信息
    modifiedMark = models.Marks.objects.filter(
            openid=databody["openid"], id=databody["routeid"]
        ).first()
    
    #如果没找到匹配的路线（正常情况下不会发生）
    if modifiedMark is None:
        return JsonResponse({
            'status': 'fail',
            'message': '路线不存在',
        })
    
    modifiedMark.title = databody["title"]
    modifiedMark.content = databody["content"]
    modifiedMark.marks = databody["marks"]

    # 获取当前时间并存储
    current_utc_time = datetime.now(timezone.utc)# 获取当前UTC时间
    beijing_time = current_utc_time + timedelta(hours=8) # 将UTC时间转换为北京时间（UTC+8）
    beijing_time = beijing_time.replace(microsecond=0)# 确保时间只精确到秒
    modifiedMark.modified_time = beijing_time
    modifiedMark.save()
    
    return JsonResponse({
        'status': 'success',
        'message': '修改路线成功',
    })
