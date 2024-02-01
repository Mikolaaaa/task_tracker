from rest_framework import serializers
from .models import Status, User, User_Task, Status_Task, Task

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name', 'description']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'patronymic', 'email']


class User_TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Task
        fields = ['id', 'worker_id', 'task_id']


class Status_TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status_Task
        fields = ['id', 'status_id', 'task_id']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'date_start', 'date_end', 'id_user', 'priority', 'readiness']

