from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'goals', views.GoalViewSet, basename='goal')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', views.GoalSummaryView.as_view(), name='goal-summary'),
    path('<int:goal_id>/contribute/', views.GoalContributionView.as_view(), name='goal-contribute'),
]
