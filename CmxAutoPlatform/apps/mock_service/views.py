import os
import re
import shutil
import subprocess

from mock_service import models
from rest_framework.views import APIView
from CmxAutoPlatform.utils.response import APIResponse
from mock_service.mock_serializes import MockProjectSer, MockUnitSer
from rest_framework.request import Request
import threading


# Create your views here.
class MockProjectViews(APIView):
    # 获取所有的专项
    def get(self, request):
        mock_project_obj = models.MockProject.objects.all()
        # 返回多条数据要加上many=True
        mock_project_ser = MockProjectSer(mock_project_obj, many=True)
        mock_project_data = mock_project_ser.data
        return APIResponse(result=mock_project_data)

    # 新增Mock专项
    def post(self, request):
        mock_project_ser = MockProjectSer(data=request.data)
        if mock_project_ser.is_valid():
            ren = mock_project_ser.save()
            projectId = ren.id
            shutil.copy("CmxAutoPlatform/apps/mock_service/mitmproxy_flows/mitm_flow.py",
                        f"CmxAutoPlatform/apps/mock_service/mitmproxy_flows/{projectId}_mitm_flow.py")
            print(ren.id)
            return self.get(request)
        else:
            return APIResponse(result="数据校验不合格")


class MockProjectView(APIView):
    # 根据项目ID获取一条项目数据
    def get(self, request, pk):
        mock_obj = models.MockProject.objects.filter(id=pk).first()
        mock_ser = MockProjectSer(mock_obj)
        data = mock_ser.data
        data['catch_log'] = eval(mock_ser.data.get("catch_log"))
        # 删除原有的记录
        # models.MockProject.objects.filter(id=pk).update(catch_log='[]')
        return APIResponse(result=data)

    # 删除专项
    def delete(self, request, pk):
        models.MockProject.objects.filter(id=pk).delete()
        # 删除mitm文件
        os.remove(f"CmxAutoPlatform/apps/mock_service/mitmproxy_flows/{pk}_mitm_flow.py")
        return MockProjectViews().get(request)


# mitm服务相关
class MitmProxyServe(APIView):
    port = 9000

    def get(self, request: Request):
        pk = request.query_params.get("projectid")
        mock_project_obj = models.MockProject.objects.filter(id=pk).first()
        # 当前服务端口号
        service_port = self.port + int(pk)
        # 获取当前平台的 ip地址
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return APIResponse(result={'state': mock_project_obj.state, 'port': str(service_port), 'ip': ip})

    def post(self, request: Request):
        pk = request.query_params.get("projectid")
        service_port = self.port + int(pk)
        # 启动服务
        if request.data.get('state') == '已关闭':
            def run_service():
                script = f"CmxAutoPlatform/apps/mock_service/mitmproxy_flows/{pk}_mitm_flow.py"
                cmd = f'nohup mitmdump -p {service_port} -s {script}'
                print(cmd)
                subprocess.call(cmd, shell=True)

            t = threading.Thread(target=run_service)
            t.start()
            # 修改数据库中的字段
            models.MockProject.objects.filter(id=pk).update(state=True)
        else:
            # 关闭服务
            print("关闭服务")
            port = str(9000 + int(pk))
            cmd = 'ps -ef|grep mitm |grep %s' % port
            res = subprocess.check_output(cmd, shell=True)
            for i in str(res).split('\\n'):
                if str(pk) + '_mitm_flow.py' in i:
                    pid = max([int(i) for i in re.findall(r'\d+', i.split('/')[0])])
                    cmd2 = 'kill -9 %s' % str(pid)
                    subprocess.check_output(cmd2, shell=True)
                    print('进程已杀死！')
                    break
            else:
                print('进程未找到！')
            models.MockProject.objects.filter(id=pk).update(state=False)

        return APIResponse(result="修改成功")


# mock单元相关
class MockUnitViews(APIView):
    # 通过项目ID查询出列表
    def get(self, request: Request):
        pk = request.query_params.get("projectid")
        unit_data = models.MockUnit.objects.filter(project_id=str(pk))
        unit_ser = MockUnitSer(unit_data, many=True)
        unit_ser_data = unit_ser.data
        return APIResponse(result=unit_ser_data)

    def post(self, request: Request):
        data = request.data
        mock_ser = MockUnitSer(data=data)
        if mock_ser.is_valid():
            mock_ser.save()
        else:
            raise "不合法"
        return self.get(request)


class MockUnitView(APIView):
    def delete(self, request: Request, pk):
        print(request.query_params.get('projectid'))
        models.MockUnit.objects.filter(id=pk).delete()
        return MockUnitViews().get(request)

    def get(self, request: Request, pk):
        print(pk)
        mock_obj = models.MockUnit.objects.filter(id=pk).first()
        mock_obj_ser = MockUnitSer(mock_obj)
        print(mock_obj_ser.data)
        return APIResponse(result=mock_obj_ser.data)

    # 保存更新
    def put(self, request: Request, pk):
        mock_ser = MockUnitSer(data=request.data)
        mock_instance = models.MockUnit.objects.filter(id=pk).first()
        if mock_ser.is_valid():
            mock_ser.update(instance=mock_instance, validated_data=mock_ser.data)
        else:
            raise "不合法"
        return MockUnitViews().get(request)
