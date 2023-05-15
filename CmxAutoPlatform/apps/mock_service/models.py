from django.db import models


# Create your models here.
# mock专项/项目
class MockProject(models.Model):
    mock_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="专项名称")
    mock_creater = models.CharField(max_length=30, null=True, blank=True, verbose_name="专项创建者")
    mock_crate_time = models.DateTimeField(null=True, verbose_name="创建的时间")
    mock_dec = models.CharField(max_length=100, null=True, blank=True, verbose_name="mock专项描述")
    # run_counts 启动次数
    run_counts = models.IntegerField(default=0)
    # 拦截成功次数
    mock_counts = models.IntegerField(default=0)
    # 项目的mitm的服务状态
    state = models.BooleanField(default=False)
    # 包的数据
    catch_log = models.TextField(default='[]')
    catch = models.BooleanField(default=False)  # 抓在线日志的开关
    black_hosts = models.CharField(max_length=500, null=True, blank=True, default='')  # 黑名单
    white_hosts = models.CharField(max_length=500, null=True, blank=True, default='')  # 白名单,不为空的时候，只放白名单域名
    catch_time = models.CharField(max_length=20, null=True, blank=True, default='')  # 最后一次在线获取抓包记录的时间戳

    def __str__(self):
        return self.mock_name


class MockUnit(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="mock单元名称")
    state = models.BooleanField(default=False, verbose_name="状态")
    project_id = models.CharField(max_length=30, null=True, blank=True, verbose_name="项目ID")
    # 请求的url
    catch_url = models.CharField(max_length=500, null=True, blank=True, default='', verbose_name="请求的URL")
    # 服务器的响应体
    mock_response_body = models.TextField(null=True, blank=True, default='', verbose_name="mock响应体")
    # 拦截模式两种：放行模式(Release) 和 拦截模式(intercept)
    model = models.CharField(max_length=30, null=True, blank=True, default='release')
    # 响应头
    response_headers = models.CharField(max_length=500, null=True, blank=True, default='{}')
    # 状态码
    state_code = models.IntegerField(default=200)
    # 拦截模式下的写死返回值
    mock_response_body_intercept = models.TextField(null=True, blank=True, default='')
    # 整个请求周期时间控制
    mock_time = models.FloatField(default=0.0)  # 整个请求周期时间控制，单位为s

    #
    def __str__(self):
        return self.name


# 项目的数据
"""
1，数据设计
数据包含哪些维度：项目包含的单元数量，mock服务启动次数，拦截成功次数。
"""
