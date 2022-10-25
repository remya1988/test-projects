from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from todoapi.serializer import UserSerializer,ToDoSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from todoapp.models import ToDos
from rest_framework import authentication,permissions
from rest_framework.decorators import action

# Create your views here.

class UserModelViewsetView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class ToDoViewsetView(ModelViewSet):
    serializer_class = ToDoSerializer
    queryset = ToDos.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def list(self,request,*args,**kwargs):
        qs=ToDos.objects.filter(user=request.user)
        serializer=ToDoSerializer(qs,many=True)
        return Response(data=serializer.data)


    def create(self,request,*args,**kwargs):
        user=request.user
        print(user)
        serializer=ToDoSerializer(data=request.data,context={"user":user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)



    def destroy(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        instance=ToDos.objects.get(id=id)
        serializer=ToDoSerializer(instance)
        instance.delete()
        return Response({"msg":"deleted"})

    def retrieve(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        qs=ToDos.objects.get(id=id)
        serializer=ToDoSerializer(qs)
        return Response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        obj=ToDos.objects.get(id=id)
        print(obj.status)
        serializer=ToDoSerializer(instance=obj,data=request.data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

