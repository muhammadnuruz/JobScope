from django.urls import path, include


urlpatterns = [
                  path('telegram-users/', include("apps.telegram_users.urls")),
                  path('companies/', include("apps.companies.urls")),
                  path('applications/', include("apps.applications.urls")),
                  path('tasks/', include("apps.tasks.urls")),
              ]
