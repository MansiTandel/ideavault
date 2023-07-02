from django.urls import path
from django.http import HttpResponse
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Home page
    path('',views.home, name=""),

    # register
    path('register', views.register,name="register"),

    # - Login
    path('my-login', views.my_login, name="my-login"),

    # - Dashboard
    path('dashboard',views.dashboard,name="dashboard"),

    # - Post idea
    path('post-idea',views.post_idea,name="post-idea"),

    # - My ideas
    path('my-ideas',views.my_ideas, name="my-ideas"),

    # - Update idea
    path('update-idea/<str:pk>',views.update_idea,name="update-idea"),

    # - Delete idea
    path('delete-idea/<str:pk>',views.delete_idea,name="delete-idea"),
    
    # -Profile management
    path('profile-management',views.profile_management,name="profile-management"),

    # - Delete account
    path('delete-account', views.delete_account, name="delete-account"),

    # - Logout
    path('user-logout', views.user_logout,name="user-logout"),

    # - 1 Allows us to enter email in order to receive a password reset link
    path('reset_password',auth_views.PasswordResetView.as_view(template_name="password-reset/password-reset.html"), name="reset_password"),

    # - 2 Show a success message starting that an email was sent to reset our password
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="password-reset/password-reset-sent.html"), name='password_reset_done'),


    # - 3 Send a link to our email, so that we can reset our password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password-reset/password-reset-form.html"), name='password_reset_confirm'),


    # - 4 Show message stating that our password was changed
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="password-reset/password-reset-complete.html"),name="password_reset_complete"),


]

