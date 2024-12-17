from django.db import models


# Create your models here.
class UserInfo(models.Model):
    openid = models.CharField(max_length=64,default="未填写")
    username = models.CharField(max_length=64,default="未填写")
    # email=models.CharField(max_length=64, default="未填写")
    # gender=models.CharField(max_length=3, default="未填写")
    # avatar_url = models.CharField(max_length=200, default="")

#     class Meta:
#         db_table = "f_user_01"
