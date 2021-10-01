from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from walet.views import UserViewSet, TransactionViewSet, TransactionAddView, UserLoginView, logout, main, profileview, \
    AccountsViewSet, cashaccount, UserTransactionView, transaction, transfer


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
    path('transfer/<str:name>/', transfer, name='transfer'),

    path('accounts/profile/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user'),
    path('api/user_transaction/<int:user>/', UserTransactionView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/transaction/<str:from_name>/<str:to_name>/', TransactionAddView.as_view()),
    path('admin/', admin.site.urls),
]
