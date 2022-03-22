from functools import partial
from logging import exception
from urllib import request
from django import views
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate
from django.http import JsonResponse
from .models import  Person, Todo
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator

from .serializers import *

# Create your views here.


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by('id')
    serializer_class = PersonSerializer

@api_view(['POST',])
def post_data(request):
    serializer = PersonSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['PUT'])
def update_data(request):
    # userid = Person.objects.get(id = id)
    # print('userid---',userid)
    serializer = PersonSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # id = serializer.data('id')
    # serializer.save()
    return Response(serializer.data)

# @api_view(['DELETE'])
# def delete_data(request,id):
#     userid = Person.objects.get(id = id)
#     print('userid---',userid)
#     serializer = PersonSerializer(userid, request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)


@api_view(['GET'])
def get_todo(request):
    data = Todo.objects.all()
    serializer = TodoSerializer(data, many=True)
    return Response({
        'status' : True,
        'data': serializer.data
    })

@api_view(['POST'])
def post_todo(request):
    try:
        serializer = TodoSerializer(data = request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({
                    'status' : True,
                    'message': 'successfully created',
                    'data': serializer.data
            })
        return Response({
            'status' : False,
            'message': 'Invaid data',
            'data': serializer.errors
        })

    except Exception as e:
        print(e)
        return Response({
            'status' : False,
            'message': 'exception error',
        })


@api_view(['PUT'])
def update_todo(request):
    try:
        data = request.data
        if not data.get('uid'):
            return Response({
                'status': False,
                'message':'uid is required',
                'data': {}
            })
        
        obj = Todo.objects.get(uid = data.get('uid'))
        serializer = TodoSerializer(obj, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status' : True,
                'message': 'successfully updated',
                'data': serializer.data
            })
        
        return Response({
            'status' : False,
            'message': 'Invaid data',
            'data': serializer.errors
        })

    except Exception as e:
        print(e)
        return Response({
            'status' : False,
            'message': 'exception error',
            'data':{}
        })


class TodoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # print(request.user.id)
        data = Todo.objects.filter(user = request.user)
        serializer = TodoSerializer(data, many=True)
        return Response({
            'status' : True,
            'message':'fetched',
            'data': serializer.data
        })

    def post(self, request):
        try:
            data = request.data
            data._mutable = True
            data['user'] = request.user.id
            data._mutable = False
            # print(request.user)
            print(data)
            serializer = TodoSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : True,
                    'message': 'successfully created',
                    'data': serializer.data
                })
            return Response({
                'status' : False,
                'message': 'Invaid data',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)
            return Response({
                'status' : False,
                'message': 'exception error',
            })

    def put(self, request):
        try:
            data = request.data
            todo_data = Todo.objects.get(uid = data.get('uid'))
            # print(request.user)
            # print(data)

            # partial=True is helpful when we have to edit a single field.
            # if dont pass partial=True then you have to pass all fields.
            serializer = TodoSerializer(todo_data, data = data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : True,
                    'message': 'successfully Updated',
                    'data': serializer.data
                })
            return Response({
                'status' : False,
                'message': 'Invaid data',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)
            return Response({
                'status' : False,
                'message': 'exception error',
            })
       

    def delete(self, request):
        try:
            data = request.data
            todo_data = Todo.objects.get(uid = data.get('uid'))
            # print(request.user)
            # print(data)
            if todo_data:
                todo_data.delete()
                return Response({
                        'status' : True,
                        'message': 'successfully Deleted',
                    })
            # partial=True is helpful when we have to edit a single field.
            # if dont pass partial=True then you have to pass all fields.
            return Response({
                'status' : False,
                'message': 'Invaid data',
                'data': todo_data.errors
            })

        except Exception as e:
            print(e)
            return Response({
                'status' : False,
                'message': 'exception error',
            })

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    @action(detail=False, methods=['GET'])
    def get_todo(self, request):
        data = TimingTodo.objects.all()
        serializer = TimingTodoSerializer(data, many=True)
        return Response({
            'status' : True,
            'message':'fetched',
            'data': serializer.data
        })

    @action(detail=False, methods=['POST'])
    # action main detail=False rakha wa q K METHOD main koi parameter ya slug pass nh kr rhy. jb koi slug pass krenge to detail=True kr denge.
    def add_date_to_todo(self, request):
        try:
            data = request.data
            serializer = TimingTodoSerializer(data = data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response({
                        'status' : True,
                        'message': 'successfully created',
                        'data': serializer.data
                })
            return Response({
                'status' : False,
                'message': 'Invaid data',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)
            return Response({
                'status' : False,
                'message': 'exception error',
            })