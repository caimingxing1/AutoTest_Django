from rest_framework.serializers import ModelSerializer
from mock_service import models


class MockProjectSer(ModelSerializer):
    class Meta:
        model = models.MockProject
        fields = "__all__"
        extra_kwargs = {
            'mock_name': {'required': True},
        }


class MockUnitSer(ModelSerializer):
    class Meta:
        model = models.MockUnit
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True},
        }