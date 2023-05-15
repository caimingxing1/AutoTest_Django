from rest_framework import serializers
from pressure import models


class PressurePlanSer(serializers.ModelSerializer):
    class Meta:
        model = models.PressurePlan
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True},
        }


class TasksSer(serializers.ModelSerializer):
    class Meta:
        model = models.Tasks
        fields = "__all__"


class ScriptsSer(serializers.ModelSerializer):
    class Meta:
        model = models.DBScripts
        fields = "__all__"
