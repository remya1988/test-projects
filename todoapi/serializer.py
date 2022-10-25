from rest_framework import serializers
from django.contrib.auth.models import User
from todoapp.models import ToDos

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password"
        ]

    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        return user

class ToDoSerializer(serializers.ModelSerializer):

    #task_name=serializers.CharField(read_only=True)
    #status=serializers.BooleanField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=ToDos
        fields=[
            "task_name",
            "status",
            "user",
        ]
    def create(self,validated_data):
        user=self.context.get("user")
        return ToDos.objects.create(**validated_data,user=user)