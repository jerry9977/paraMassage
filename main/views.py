import base64
from inspect import signature
from django.shortcuts import render, redirect
from paraMassage.settings import BASE_DIR

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
import os
from urllib import request as req
from django.core.files.uploadedfile import InMemoryUploadedFile
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
            return redirect("/form_submitted/", request)
    else:
        form = f.CustomerCheckInForm()

    context = {
        'form':form
    }
    return render(request, 'form/customer_check_in_form.html', context)

def remedial_check_in_form(request):

    if request.method =="POST":

        

        # post = request.POST.copy() # to make it mutable
        area_of_soreness_front = request.POST.get("area_of_soreness_front")
        area_of_soreness_back = request.POST.get("area_of_soreness_back")
        signature = request.POST.get("signature")
        # print(area_of_soreness)
        with req.urlopen(area_of_soreness_front) as response:
            data = response.read()

        with open("image.png", "wb") as area_of_soreness_front_image:
            area_of_soreness_front_image.write(data)

        with req.urlopen(area_of_soreness_back) as response:
            data1 = response.read()
        with open("image2.png", "wb") as area_of_soreness_back_image:
            area_of_soreness_back_image.write(data1)

        # area_of_soreness_front_image.close()
        request.FILES["area_of_soreness_front"] = InMemoryUploadedFile(file=data, field_name="front_image", name="front", content_type="image/jpg",size=data, charset="base64")
        request.FILES["area_of_soreness_back"] = InMemoryUploadedFile(file=data, field_name="front_image", name="front", content_type="image/jpg",size=data, charset="base64")
        area_of_soreness_front_image.close()
        print(request.FILES)
        # or set several values from dict
        # post.update({'postvar': 'some_value', 'var': 'value'})
        # # or set list
        # post.setlist('list_var', ['some_value', 'other_value']))

        # # and update original POST in the end
        # request.POST = post

        remedial_history_form = f.RemedialHistoryForm(request.POST, request.FILES)
        client_form = f.CustomerCheckInForm(request.POST)
        remedial_form = f.RemedialCustomerCheckInForm(request.POST)
        # print(request.POST)
        # print(remedial_history_form.is_valid())
        if remedial_history_form.is_valid() and client_form.is_valid() and remedial_form.is_valid():

            client = client_form.save()
            remedial_client_info = remedial_form.save(commit=False)
            remedial_client_history = remedial_history_form.save(commit=False)
            
            remedial_client_info.client = client
            remedial_client_info.save()

            remedial_client_history.remedial_client_info = remedial_client_info
            remedial_client_history.save()

            return redirect("/form_submitted/", request)
    else:
        client_form = f.CustomerCheckInForm() 
        remedial_history_form = f.RemedialHistoryForm()
        remedial_form = f.RemedialCustomerCheckInForm()
    
    context = {
        "client_form": client_form,
        "remedial_history_form":remedial_history_form,
        "remedial_form": remedial_form
    }
    return render(request, 'form/remedial_check_in_form.html', context)


def form_submitted(request):
    context = {}
    return render(request, 'form/remedial_check_in_form.html', context)


def upload_receipt(request):

    if request.method == "POST":

        if request.FILES.get("image", None) is not None:
            remedial_history_id = request.POST.get("id")
            img = request.FILES["image"]
            
            try:
                print("==============")
                print("==============")
                print("==============")
                print("==============")
                
                # img_file = open(os.path.join(settings.MEDIA_ROOT, "123"),'wb')
                
                print("1")
                # img_file.write(img.read())
                
                remedial_history = m.RemedialMedicalHistory.objects.get(pk=remedial_history_id)
                
                print("2")
                remedial_history.receipt_image.save(
                    "remedial_receipt.jpg",
                    img
                )

                print("3")
                remedial_history.save()
                # print(settings.BASE_DIR)
                # print(os)
                # print(os.path)
                # print(os.path.join(settings.MEDIA_ROOT))
                # print()

                print(remedial_history.receipt_image.name)
                print(remedial_history.receipt_image.path)
                # print(remedial_history.recept_image.path)
                print("==============")
                print("==============")

                response = HttpResponse()
                response['Content-Type'] = 'application/json'
                return response

            except Exception as e:
                print(e)
                pass

            
    response = HttpResponse()
    response['Content-Type'] = 'application/json'
    return response


