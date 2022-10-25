from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView
from todoapp import forms
from django.urls import reverse_lazy
from todoapp.models import ToDos
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from todoapp.decorators import signin_required
from django.utils.decorators import method_decorator

# class SignUpView(View):
#     def get(self,request,*args,**kwargs):
#         form=forms.RegistrationForm()
#         return render(request,"registration.html",{"form":form})
#
#     def post(self,request,*args,**kwargs):
#         form=forms.RegistrationForm(request.POST)
#         if form.is_valid():
#             User.objects.create_user(**form.cleaned_data)
#             return redirect("signin")
#         else:
#             return render(request,"registration.html",{"form":form})

class SignUpView(CreateView):
    model = User
    form_class = forms.RegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"User added successfully.")
        return super().form_valid(form)

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=forms.LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=forms.LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(uname,pwd)
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                messages.success(request,"You are In..")
                return redirect("index")
            else:
                messages.error(request,"Invalid Username or Password.")
                return render(request, "login.html",{"form":form})
@method_decorator(signin_required,name="dispatch")
class IndexView(TemplateView):
    # def get(self,request,*args,**kwargs):
    #     return render(request,"home.html")   or can use templetae view
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["todos"]=ToDos.objects.filter(user=self.request.user,status=False)
        return context

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
# Create Add todo View
# class ToDoAddView(View):
#     def get(self,request,*args,**kwargs):
#         form=forms.ToDoForm()
#         return render(request,"add-todo.html",{"form":form})
#     def post(self,request,*args,**kwargs):
#         form=forms.ToDoForm(request.POST)
#         if form.is_valid():
#             form.instance.user=request.user
#             form.save()
#             return redirect("index")
#         else:
#             return render(request,"add-todo.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class ToDoAddView(CreateView):
    model=ToDos
    form_class = forms.ToDoForm
    template_name = "add-todo.html"
    success_url = reverse_lazy("todolist")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"Todo has been successfully added.")
        return super().form_valid(form)



# class ToDoListView(View):
#     def get(self,request,*args,**kwargs):
#         all_todos=ToDos.objects.filter(user=request.user)
#
#         return render(request,"todolist.html",{"todos":all_todos})

# Instead of using View class we can use predefined ListView for listing todos

@method_decorator(signin_required,name="dispatch")
class ToDoListView(ListView):
    model = ToDos
    context_object_name = "todos"
    template_name = "todolist.html"

    def get_queryset(self):
        return ToDos.objects.filter(user=self.request.user)

@signin_required
def delete_todo(request,*args,**kwargs):
    id=kwargs.get("id")
    ToDos.objects.get(id=id).delete()
    return redirect("todolist")

# class TodoDetailView(View):
#     def get(self,request,*args,**kwargs):
#         id=kwargs.get("id")
#         todo=ToDos.objects.get(id=id)
#         return render(request,"todo-detail.html",{"todo":todo})

@method_decorator(signin_required,name="dispatch")
class TodoDetailView(DetailView):
    model=ToDos
    context_object_name = "todo"
    template_name = "todo-detail.html"
    pk_url_kwarg = "id"        #in url map <int:id> for maping pk to id use this

# class TodoEditView(View):
#     def get(self,request,*args,**kwargs):
#         id = kwargs.get("id")
#         todo=ToDos.objects.get(id=id)
#         form=forms.ToDoChangeForm(instance=todo)
#         return render(request,"todo-update.html",{"form":form})
#     def post(self,request,*args,**kwargs):
#         id = kwargs.get("id")
#         todo = ToDos.objects.get(id=id)
#         form=forms.ToDoChangeForm(request.POST,instance=todo)
#         if form.is_valid():
#             form.save()
#             msg="To do has been changed...."
#             messages.success(request, msg)
#             return redirect("todolist")
#         else:
#             msg="To do updation failed......"
#             messages.error(request, msg)
#             return render(request,"todo-update.html",{"form":form})


@method_decorator(signin_required,name="dispatch")
class TodoEditView(UpdateView):
    model = ToDos
    form_class = forms.ToDoChangeForm
    template_name = "todo-update.html"
    success_url = reverse_lazy("todolist")
    pk_url_kwarg = "id"

    def form_valid(self, form):
        messages.success(self.request,"Todo updated.")
        return super().form_valid(form)

