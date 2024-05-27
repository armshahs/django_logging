from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Todo
from .serializers import TodoSerializer


# Create your views here.
@api_view(["GET"])
def get_todos(request):
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Rewriting the above in GenericAPIView
class get_todos_generics(generics.GenericAPIView):

    def get(self, request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def post_todo(request):

    # owner id 1 is admin. Since we do not have auth, this is a workaround
    owner_id = 1
    owner = get_object_or_404(User, id=owner_id)

    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=owner)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(
        {"message": "Request failed, please try again"},
        status=status.HTTP_400_BAD_REQUEST,
    )


# Rewriting the post request in GenericAPIView
class post_todo_generics(generics.GenericAPIView):

    def post(self, request):

        # owner id 1 is admin. Since we do not have auth, this is a workaround
        owner_id = 1
        owner = get_object_or_404(User, id=owner_id)

        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"message": "Request failed, please try again"},
            status=status.HTTP_400_BAD_REQUEST,
        )
