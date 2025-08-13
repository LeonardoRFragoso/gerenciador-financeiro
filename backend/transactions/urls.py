from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'transactions', views.TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', views.TransactionSummaryView.as_view(), name='transaction-summary'),
    path('monthly-report/', views.MonthlyReportView.as_view(), name='monthly-report'),
    path('categories-report/', views.CategoriesReportView.as_view(), name='categories-report'),
]
