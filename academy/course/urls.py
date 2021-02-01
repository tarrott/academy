from django.urls import path

from .views import (
    HomePageView,
    ResourceDetailView,
    DashboardView,
    FeedbackListView,
    FeedbackUserListView,
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackDelete
)


urlpatterns = [
    path('', HomePageView.as_view(), name='course_home'),
    path('resource/', HomePageView.as_view(), name='resource'),
    path('resource/<int:pk>/', ResourceDetailView.as_view(), name='resource_detail'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/feedback/', FeedbackListView.as_view(), name='feedback'),
    path('dashboard/feedback/<str:username>', FeedbackUserListView.as_view(), name='user_feedback'),
    path('feedback/new/', FeedbackCreate.as_view(), name='feedback_create'),
    path('feedback/<int:pk>/edit/', FeedbackUpdate.as_view(), name='feedback_edit'),
    path('feedback/<int:pk>/delete/', FeedbackDelete.as_view(), name='feedback_delete'),
]
