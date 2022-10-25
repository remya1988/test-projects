from django.urls import path
from todoapp import views

urlpatterns=[
    path("signup",views.SignUpView.as_view(),name="register"),
    path("login",views.LoginView.as_view(),name="signin"),
    path("home",views.IndexView.as_view(),name="index"),
    path("signout",views.SignOutView.as_view(),name="signout"),
    path("todos/add",views.ToDoAddView.as_view(),name="add-todo"),
    path("todos/list",views.ToDoListView.as_view(),name="todolist"),
    path("todos/remove/<int:id>",views.delete_todo,name="remove-todo"),
    path("todos/detail/<int:id>",views.TodoDetailView.as_view(),name="todo-details"),
    path("todo/change/<int:id>",views.TodoEditView.as_view(),name="todo-update"),
]