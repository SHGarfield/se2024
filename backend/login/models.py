from django.db import models


# Create your models here.
class UserInfo(models.Model):
    openid = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    email=models.CharField(max_length=64, default="未填写")
    gender=models.IntegerField(max_length=1, default=0)

#     class Meta:
#         db_table = "f_user_01"
