import base64
from inspect import signature
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
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
import datetime
import json

from main.image_verifier.image_verifier import ImageVerifier

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

def customer_view(request, id):
    client = m.Client.objects.filter(pk=id)
    client_remedial_detail = m.RemedialClientInfo.objects.filter(client=client.first())
    client_remedial_history = m.RemedialMedicalHistory.objects.filter(remedial_client_info=client_remedial_detail.first())
    
    client = client.values().first()
    client_remedial_detail = client_remedial_detail.values().first()
    client_remedial_history = client_remedial_history

    # print(client["id"])
    client_info = {
        "first_name": client["first_name"],
        "last_name": client["last_name"],
        "email": client["email"],
        "DOB": client["DOB"],
        "mobile": str(client["mobile"]),
        "home_phone": str(client["home_phone"]),
        "health_insurance_number": str(client_remedial_detail["health_insurance_number"]),
        "suffix": str(client_remedial_detail["suffix"]),
        "gender": client_remedial_detail["gender"],
        "martial_status": client_remedial_detail["martial_status"],
        "weight": str(client_remedial_detail["weight"]),
        "height": str(client_remedial_detail["height"]),
        "children": client_remedial_detail["children"],
        "occupation": client_remedial_detail["occupation"],
        "address": client_remedial_detail["address"],
        "job": client_remedial_detail["job"],
        "emergency_contact_number": client_remedial_detail["emergency_contact_number"],
        "emergency_contact_name": client_remedial_detail["emergency_contact_name"],
        "date_created": datetime.datetime.strftime(client["date_created"], "%d %b %Y %H:%M"),
    }

    history_container = []
    for history in client_remedial_history:
        history_container.append({
            "id": history.id,
            "area_of_soreness_front":history.area_of_soreness_front.url if history.area_of_soreness_front else "",
            "area_of_soreness_back":history.area_of_soreness_back.url if history.area_of_soreness_back else "",
            "reason_of_visit": history.reason_of_visit,
            "symptoms": history.symptoms,
            "medication": history.medication,
            "health_care": history.health_care,
            "additional_comments": history.additional_comments,

            # "reason_of_visit": hist_val["reason_of_visit"],
            # "symptoms": hist_val["symptoms"],
            # "medication": hist_val["medication"],
            # "health_care": hist_val["health_care"],
            # "additional_comments": hist_val["additional_comments"],
            "signature": history.signature.url if history.signature else "",
            "date_created": datetime.datetime.strftime(history.date_created, "%d %b %Y %H:%M")
            # "date_created": datetime.datetime.strftime(hist_val["date_created"], "%d %b %Y %H:%M")
        })

    context = {
        "client_info": client_info,
        "client_remedial_history": json.dumps(history_container)
    }
    return render(request, 'main/client_view.html', context)


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

        area_of_soreness_front = request.POST.get("area_of_soreness_front_hidden")
        area_of_soreness_back = request.POST.get("area_of_soreness_back_hidden")
        signature = request.POST.get("signature_hidden")

        
       
        remedial_history_form = f.RemedialHistoryForm(request.POST, request.FILES)
        client_form = f.CustomerCheckInForm(request.POST)
        remedial_form = f.RemedialCustomerCheckInForm(request.POST)

        front_image = ImageVerifier(area_of_soreness_front, field_name="area_of_soreness_front", allow_null=True, form=remedial_history_form)
        back_image = ImageVerifier(area_of_soreness_back, field_name="area_of_soreness_back", allow_null=True, form=remedial_history_form)
        signature_image = ImageVerifier(signature, field_name="signature", allow_null=False, form=remedial_history_form)


        if front_image.is_valid() and back_image.is_valid() and signature_image.is_valid():
            if remedial_history_form.is_valid() and client_form.is_valid() and remedial_form.is_valid():

                client = client_form.save()
                remedial_client_info = remedial_form.save(commit=False)
                remedial_client_history = remedial_history_form.save(commit=False)
                
                remedial_client_info.client = client
                remedial_client_info.save()

                
                remedial_client_history.remedial_client_info = remedial_client_info
                
                if front_image.memory_file:

                    remedial_client_history.area_of_soreness_front.save(
                        "remedial_front.jpg",
                        front_image.memory_file,
                        save=False
                    )
                if back_image.memory_file:

                    remedial_client_history.area_of_soreness_back.save(
                        "remedial_back.jpg",
                        back_image.memory_file,
                        save=False
                    )

                remedial_client_history.signature.save(
                    "remedial_signature.jpg",
                    signature_image.memory_file,
                    save=False
                )
                remedial_client_history.save()

                return redirect("form_submitted", title="Client Intake Form")
            else:
                remedial_history_form = f.RemedialHistoryForm(
                request.POST, 
                request.FILES, 
                initial={
                    "area_of_soreness_front":area_of_soreness_front,
                    "area_of_soreness_back": area_of_soreness_back,
                    "signature":signature
                }
            )

    else:
        client_form = f.CustomerCheckInForm() 
        remedial_history_form = f.RemedialHistoryForm()
        remedial_form = f.RemedialCustomerCheckInForm()
    
    # print(request.POST)
    
    context = {
        "client_form": client_form,
        "remedial_history_form":remedial_history_form,
        "remedial_form": remedial_form
    }
    return render(request, 'form/remedial_check_in_form.html', context)


def form_submitted(request, title):
    context = {"title":title}
    return render(request, 'form/form_submitted.html', context)


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
                    img,
                    save=False
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




class ClientListView(ListView):
    model = m.RemedialClientInfo
    template_name = 'main/client_list.html'
    paginate_by = 2
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_json = []
        for remedial_client in context["object_list"]:
            client_json.append({
                "id": remedial_client.client.id,
                "first_name": remedial_client.client.first_name,
                "last_name": remedial_client.client.last_name,
                "health_insurance_number": str(remedial_client.health_insurance_number),
                "suffix": str(remedial_client.suffix),
                "date_created": datetime.datetime.strftime(remedial_client.client.date_created, "%d %b %Y %H:%M")

            })
        context["client_json"] = json.dumps(client_json)
        
        paginator = context["page_obj"]

        start_page, end_page = self._get_start_end_page(paginator.paginator.num_pages, paginator.number)
        context["paginator_range"] = range(start_page, end_page + 1)
        print(context)
        return context

    def _get_start_end_page(self, total_pages, current_page):
        max_page = 5

        if total_pages <= max_page:
            start_page = 1
            end_page = total_pages
        else:
            max_page_before_current = 2
            max_page_after_current = 2

            if current_page <= max_page_before_current + 1:
                start_page = 1
                end_page = max_page
            elif current_page + max_page_after_current >= total_pages:
                start_page = total_pages - max_page + 1
                end_page = total_pages
            else:
                start_page = current_page - max_page_before_current
                end_page = current_page + max_page_after_current
        
        return start_page, end_page