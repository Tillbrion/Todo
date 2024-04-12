from django.urls import path
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,DeleteView,CustomLoginView,SignUpForm,DeleteTasksView, VerificationView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', SignUpForm.as_view(), name='register'),
    path('',TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    path('delete_tasks/<int:pk>/', DeleteTasksView.as_view(), name='delete_tasks'),
    path('verify-account', VerificationView.as_view(), name='verify'),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='todoapp/reset_password.html'), name= 'reset_password'), #submit email form
    path('reset_password_bsent/', auth_views.PasswordResetDoneView.as_view(template_name='todoapp/reset_password_done.html'), name='password_reset_done'), #email sent success message
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='todoapp/reset_password_form.html'), name='password_reset_confirm'), #link to password reset in email
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='todoapp/reset_password_complete.html'),name='password_reset_complete'), #password successfully changed



]