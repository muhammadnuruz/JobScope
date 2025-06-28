from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from datetime import datetime, date

from apps.companies.models import Companies
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer, TaskListSerializer, TaskListSerializer2
from apps.telegram_users.models import TelegramUsers


class TaskDeleteAPIView(DestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [AllowAny]


class TaskCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TaskListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"detail": "user_id required"}, status=400)

        tasks = Task.objects.filter(user_id=user_id).order_by('-created_at')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class CompleteTaskAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"detail": "Задача не найдена."}, status=404)
        task.completed_at = datetime.now()
        deadline = task.deadline
        if isinstance(deadline, datetime):
            deadline_date = deadline.date()
        elif isinstance(deadline, date):
            deadline_date = deadline
        else:
            deadline_date = datetime.strptime(str(deadline), '%Y-%m-%d').date()
        completed_date = task.completed_at.date()
        user = task.user
        if completed_date <= deadline_date:
            user.point += task.reward
        else:
            user.fine += task.penalty
        user.save()
        task_title = task.title
        task_company = task.company.name if task.company else "—"
        task.delete()
        return Response({
            "detail": "Задача успешно завершена и удалена.",
            "title": task_title,
            "company": task_company
        }, status=200)


class TasksByCompanyAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, company_id):
        try:
            company = Companies.objects.get(pk=company_id)
        except Companies.DoesNotExist:
            return Response({"detail": "Компания не найдена"}, status=404)

        tasks = Task.objects.filter(company=company)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)


class MyTasksAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        chat_id = request.query_params.get("chat_id")
        if not chat_id:
            return Response({"detail": "chat_id is required"}, status=400)
        tasks = Task.objects.filter(user=chat_id)
        serializer = TaskListSerializer2(tasks, many=True)
        return Response(serializer.data)
