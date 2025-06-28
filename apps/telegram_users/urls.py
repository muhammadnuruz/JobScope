from django.urls import path

from apps.telegram_users.views import TelegramUsersDetailViewSet, TelegramUsersChatIdDetailViewSet, \
    TelegramUsersUpdateViewSet, TelegramUsersCreateViewSet, TelegramUsersListViewSet, \
    NearbyUsersView, UserManagerCompaniesAPIView, UserEmployeeCompaniesAPIView, AddFavouriteCompanyAPIView, \
    EmployeesByCompanyView

urlpatterns = [
    path('', TelegramUsersListViewSet.as_view(),
         name='telegram-users-list'),
    path('create/', TelegramUsersCreateViewSet.as_view(),
         name='telegram-users-create'),
    path('chat_id/<str:chat_id>/', TelegramUsersChatIdDetailViewSet.as_view(),
         name='telegram-users-chat_id'),
    path('detail/<int:pk>/', TelegramUsersDetailViewSet.as_view(),
         name='telegram-users-detail'),
    path('update/<int:pk>/', TelegramUsersUpdateViewSet.as_view(),
         name='telegram-users-update'),
    path('employees/<int:company_id>/', EmployeesByCompanyView.as_view(), name='employees-by-company'),
    path('nearby-users/', NearbyUsersView.as_view(), name='nearby-users'),
    path('manager-companies/<int:chat_id>/', UserManagerCompaniesAPIView.as_view(), name='manager-companies'),
    path('employee-companies/<int:chat_id>/', UserEmployeeCompaniesAPIView.as_view(), name='employee-companies'),
    path('favourites/', AddFavouriteCompanyAPIView.as_view(), name='favourites-manage'),
]
