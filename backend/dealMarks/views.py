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
    if request.method == 'POST':
        databody = json.loads(request.body)
        print("databody:",databody)
        
        # 创建一个新的实例并存储JSON数组数据
        new_instance = models.Marks()
        new_instance.openid = databody['openid']
        new_instance.title = databody['title']
        new_instance.content = databody['content']
        new_instance.marks=databody['marks']
        new_instance.isprivate=databody['isprivate']

        # 获取当前UTC时间
        current_utc_time = datetime.now(timezone.utc)
        # 将UTC时间转换为北京时间（UTC+8）
        beijing_time = current_utc_time + timedelta(hours=8)
        # 确保时间只精确到秒
        beijing_time = beijing_time.replace(microsecond=0)
        new_instance.modified_time = beijing_time
        new_instance.save()
        
        # 获取所有条目
        all_entries = models.Marks.objects.all()

        # 遍历条目并访问具体信息
        for entry in all_entries:
            print(models.Marks.objects.all().values('id', 'title'))
            print(entry.openid, entry.title, entry.content, entry.marks, entry.modified_time)
        getMarks(request)
    return JsonResponse({'status': 'success'})

def getMarks(request):
    if request.method == 'POST':
        databody = json.loads(request.body)
        print("databody:",databody)
        
        isprivate = databody.get('isprivate')
        openid = databody.get('openid')
        # 过滤出所有符合条件的条目
        if isprivate:
            matching_entries = models.Marks.objects.filter(openid=openid,isprivate=True)
        else:
            matching_entries = models.Marks.objects.filter(openid=openid,isprivate=False)
        
        # 将查询集转换为列表
        entries_list = list(matching_entries.values('id', 'modified_time','title','content','marks'))  # 根据需要选择字段
        print("entried_list:",entries_list)
        # 将列表作为JSON响应发送到请求端
        return JsonResponse({'data': entries_list}, safe=False)
    
# def getAllMarks(request):
#     if request.method == 'POST':
#         databody = json.loads(request.body)
#         print("databody:",databody)
        
#         openid = databody.get('openid')
#         # 过滤出所有符合条件的条目
#         matching_entries = models.Marks.objects.filter(isprivate=False)
        
#         # 将查询集转换为列表
#         entries_list = list(matching_entries.values('id', 'modified_time','title','content','marks'))  # 根据需要选择字段
#         print("entried_list:",entries_list)
#         # 将列表作为JSON响应发送到请求端
#         return JsonResponse({'data': entries_list}, safe=False)

@require_http_methods(["GET"])
def getAllMarks(request):
    # 过滤出所有符合条件的条目（非私有的）
    matching_entries = models.Marks.objects.filter(isprivate=False)
    
    # 将查询集转换为列表
    entries_list = list(matching_entries.values('id', 'modified_time', 'title', 'content', 'marks'))
    print("entried_list:",entries_list)
    # 将列表作为JSON响应发送到请求端
    return JsonResponse({'data': entries_list}, safe=False)
    