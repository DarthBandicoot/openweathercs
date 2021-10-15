from django.urls import path

from todo.views import TodoListView, ActiveTaskView, AccountView, AddTaskView, EditTaskView, delete_task

app_name = 'todo-list'

urlpatterns = [

    path('', AccountView.as_view(), name='select_account'),
    path('<str:todo_list_id>', TodoListView.as_view(), name='todo_list'),
    path('<str:todo_list_id>/task/create/', AddTaskView.as_view(), name="create_task"),
    path('<str:todo_list_id>/task/edit/<str:pk>', EditTaskView.as_view(), name="edit_task"),
    path('<str:todo_list_id>/task/delete/<str:pk>', delete_task, name="delete_task"),
    path('<str:todo_list_id>/task/view/<str:pk>', ActiveTaskView.as_view(), name="active_task"),

]
