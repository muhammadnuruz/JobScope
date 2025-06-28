from rest_framework import serializers
from apps.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class TaskListSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'deadline', 'reward', 'penalty', 'status', 'user_name']

    def get_user_name(self, obj):
        return obj.user.full_name or obj.user.username or str(obj.user.chat_id)


class TaskListSerializer2(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    description = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    deadline = serializers.DateField(read_only=True)
    reward = serializers.IntegerField(read_only=True)
    penalty = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'company_name',
            'deadline',
            'reward',
            'penalty',
            'status',
        ]
