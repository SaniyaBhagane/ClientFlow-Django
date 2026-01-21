from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.add_client, name='add_client'),
    path('clients/<int:client_id>/projects/', views.project_list, name='project_list'),
    path('clients/<int:client_id>/projects/add/', views.add_project, name='add_project'),
    # Tasks
    path(
        'projects/<int:project_id>/tasks/',
        views.task_list,
        name='task_list'
    ),
    path(
        'projects/<int:project_id>/tasks/add/',
        views.add_task,
        name='add_task'
    ),
    path(
        'tasks/<int:task_id>/update/',
        views.update_task,
        name='update_task'
    ),
    path(
        'tasks/<int:task_id>/delete/',
        views.delete_task,
        name='delete_task'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(
        template_name='core/login.html'
    ), name='login'),
]
