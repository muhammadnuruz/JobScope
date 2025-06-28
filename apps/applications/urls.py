from django.urls import path
from apps.applications.views import ApplicationCreateAPIView

urlpatterns = [
    path('applications/create/', ApplicationCreateAPIView.as_view(), name='application-create'),
]
