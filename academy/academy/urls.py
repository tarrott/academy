from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from users.views import (
    RegisterFormView,
    AccountView,
    PaymentDelete,
    session_enrollment,
    PaymentUpdate
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='course/home.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('account/', AccountView.as_view(), name='account'),
    path('enrollment/create/', session_enrollment, name='session_enrollment'),
    path('enrollment/<int:pk>/delete/', PaymentDelete.as_view(), name='enrollment_delete'),
    path('enrollment/<int:pk>/edit/', PaymentUpdate.as_view(), name='payment_update'),
    path('', include('course.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
