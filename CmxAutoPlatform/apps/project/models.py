from django.db import models


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="项目名称")
    creater = models.CharField(max_length=30, null=True, blank=True, verbose_name="创建者")
    create_time = models.DateTimeField(null=True, verbose_name="创建的时间")
    mock_dec = models.CharField(max_length=100, null=True, blank=True, verbose_name="项目描述")

    def __str__(self):
        return self.name
