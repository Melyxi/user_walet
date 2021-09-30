"""user_walet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from walet.views import UserViewSet, TransactionViewSet, TransactionAddView, UserLoginView, logout, main, profileview, \
    AccountsViewSet, cashaccount, UserTransactionView, transaction

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('transaction', TransactionViewSet)
router.register('cashaccounts', AccountsViewSet)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('', main, name='main'),
    path('accounts/<int:pk>/', profileview, name='profile'),
    path('cashaccounts/<int:pk>/', cashaccount, name='cashaccount'),
    path('transaction/<int:pk>/', transaction, name='transaction'),


    path('accounts/profile/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user'),

    path('api/user_transaction/<int:user>/', UserTransactionView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/transaction/<str:from_name>/<str:to_name>/', TransactionAddView.as_view()),
    path('admin/', admin.site.urls),
]
