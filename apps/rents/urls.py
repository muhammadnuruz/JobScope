from django.urls import path
from .views import DebtCreateView, DebtListView, DebtDeleteAPIView

urlpatterns = [
    path('create/', DebtCreateView.as_view(), name='debt-create'),
    path('', DebtListView.as_view(), name='debt-list'),
    path("delete/<int:pk>/", DebtDeleteAPIView.as_view(), name="debt-delete"),
]
