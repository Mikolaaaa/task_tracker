from django.urls import path
from .views import status_list, status_task_list, task_list, user_list, user_task_list, create_status, create_task, \
    create_user, create_task_status, create_task_user, UserTaskList, update_task, update_user, update_status, \
    update_user_task, update_task_status, UserList, delete_stasus, delete_user_task, delete_task, delete_user, \
    delete_stasus_task

urlpatterns = [

    path('tasks/', task_list.as_view()),
    path('tasks/add/', create_task),
    path('tasks/<int:user_id>/', UserTaskList.as_view()),
    path('uptasks/<int:id>/', update_task),
    path('deltasks/<int:id>/', delete_task),


    path('api/users/', user_list.as_view()),
    path('api/users/add/', create_user),
    path('upuser/<int:id>/', update_user),
    path('deluser/<int:id>/', delete_user),

    path('api/users/<int:id>/', UserList.as_view()),


    path('statuses/', status_list.as_view()),
    path('statuses/add/', create_status),
    path('upstatuses/<int:id>/', update_status),
    path('delstatuses/<int:id>/', delete_stasus),


    path('user_task/', user_task_list.as_view()),
    path('user_task/add', create_task_user),
    path('upuser_task/<int:id>/', update_user_task),
    path('deluser_task/<int:id>/', delete_user_task),


    path('status_task/', status_task_list.as_view()),
    path('status_task/add/', create_task_status),
    path('upstatus_task/<int:id>/', update_task_status),
    path('delstatus_task/<int:id>/', delete_stasus_task),



]
