from django.db import models
# 如果你使用的是SQLite，Django 3.1及以上版本已经内置了JSONField
# from django.db.models import JSONField

# Create your models here.

class Marks(models.Model):
    openid = models.CharField(max_length=64)
    modified_time = models.DateTimeField()
    title=models.CharField(max_length=20)
    content=models.CharField(max_length=210)
    marks = models.JSONField()
    isprivate = models.BooleanField(default=True)
    