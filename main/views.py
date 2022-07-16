import email
from lib2to3.pgen2 import token
from urllib import response
from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.middleware import csrf
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings


from django.http import HttpResponse
from django.template import loader, RequestContext
import main.models as m
import main.forms as f
import jwt 

import json

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class refreshToken(APIView):
    def post(self,request):
        data = request.data
        response = Response()
        token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        jwt.decode(
            token,
            settings.SIMPLE_JWT['SIGNING_KEY'],
            algorithms=[settings.SIMPLE_JWT['ALGORITHM']],
        )

class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        response = Response()        
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                    value = data["access"],
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = {"Success" : "Login successfully","data":data}
                return response
            else:
                return Response({"No active" : "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)



def standard_login(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next = request.GET.get("next")
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print(e)
            context = {
                "error": json.dumps("User or password does not exist.")
            }
            return render(request, 'main/login.html', context)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if next:
                return redirect(next)
            return redirect('/dashboard/')

        else:
            context = {
                "error": json.dumps("User or password does not exist.")
            }
            return render(request, 'main/login.html', context)
    
    # template = loader.get_template('main/login.html')
    context = {}
    return render(request, 'main/login.html', context)

@login_required(login_url='/login/')
def dashboard(request):

    context = {}
    return render(request, 'main/dashboard.html', context)


@login_required(login_url='/login/')
def customer_list(request):

    context = {}
    return render(request, 'main/customer_list.html', context)


@login_required(login_url='/login/')
def check_in(request):
    # token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
    # jwt.decode(
    #     token,
    #     settings.SIMPLE_JWT['SIGNING_KEY'],
    #     algorithms=[settings.SIMPLE_JWT['ALGORITHM']],
    # )

    # template = loader.get_template('main/check_in.html')
    # context = {}
    # return HttpResponse(template.render(context,request))

    context = {}
    return render(request, 'main/check_in.html', context)


def customer_check_in_form(request):
    if request.method == "POST":
        form = f.CustomerCheckInForm(request.POST)

        if form.is_valid():
            form.save()
            redirect("/form_submitted/")
        
        # m.objects.filter()
    else:
        form = f.CustomerCheckInForm()

    context = {
        'form':form
    }
    return render(request, 'form/customer_check_in_form.html', context)

def remedial_check_in_form(request):
    context = {}
    return render(request, 'form/remedial_check_in_form.html', context)


def form_submitted(request):
    context = {}
    return render(request, 'form/remedial_check_in_form.html', context)