from django.db import models


# Create your models here.
class UserInfo(models.Model):
    openid = models.CharField(max_length=64,default="未填写")
    username = models.CharField(max_length=15,default="未填写")
