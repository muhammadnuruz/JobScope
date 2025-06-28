from django.urls import path
from apps.tasks.views import TaskCreateView, TaskListView, TasksByCompanyAPIView, TaskDeleteAPIView, \
    MyTasksAPIView, CompleteTaskAPIView

urlpatterns = [
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/list/', TaskListView.as_view(), name='task-list'),
    path("tasks/<int:task_id>/complete/", CompleteTaskAPIView.as_view(), name="complete-task"),
    path('tasks/by-company/<int:company_id>/', TasksByCompanyAPIView.as_view(), name='tasks-by-company'),
    path('tasks/<int:pk>/delete/', TaskDeleteAPIView.as_view(), name='task-delete'),
    path("my-tasks/", MyTasksAPIView.as_view(), name="my-tasks"),
]
