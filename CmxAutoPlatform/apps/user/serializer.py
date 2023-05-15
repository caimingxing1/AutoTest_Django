from rest_framework import serializers

from . import models


class UserSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'password']
