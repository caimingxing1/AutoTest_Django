from rest_framework import serializers

from project import models


class ProjectSer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = "__all__"
