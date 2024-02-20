from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.middleware import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.utils.decorators import method_decorator

from django.http import HttpResponse
from django.template import loader, RequestContext
import main.models as m
import main.forms as f
import jwt 
import datetime
import json

from main.image_verifier.image_verifier import ImageVerifier, CustomMemoryFile
from django.db.models import Q

from io import BytesIO
from PIL import Image
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
        force_login = request.POST.get("force-login", False)
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

            user_profile, _ = m.UserProfile.objects.get_or_create(user=user)
        
            if user_profile.has_logged_in() and not force_login:
                context = {
                    "already_logged_in": json.dumps(True),
                    "password":password,
                    "username":username
                }
                return render(request, 'main/login.html', context)

            if user_profile.has_multiple_login_attempt():
                context = {
                    "error": json.dumps("Your account has temporarily locked due frequent login attempt.")
                }
                return render(request, 'main/login.html', context)
                
            user_profile.handle_duplicate_logins()

            login(request, user)

            hist = m.LoginHistory()
            hist.user = user
            hist.login_time = datetime.datetime.now()

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                hist.remote_addr = x_forwarded_for.split(',')[0]
            else:
                hist.remote_addr = request.META.get('REMOTE_ADDR')
            hist.session_key = request.session.session_key
            hist.save()

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

def standard_logout(request):
    logout(request)
    return render(request, 'main/login.html')

@login_required(login_url='/login/')
def dashboard(request):
    from django.db.models import Count
    from django.db.models.functions import TruncDate

    today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
    seven_days_ago = today - datetime.timedelta(days=7)
    # recently added remedial client  
    total_count_last_seven_days = m.ClientDetailInfo.objects\
        .select_related("client")\
        .filter(date_created__lt=today, date_created__gte=seven_days_ago)\
        .annotate(registered_date=TruncDate('date_created'))\
        .order_by('registered_date')\
        .values("registered_date")\
        .annotate(**{'total': Count('registered_date')})

    seven_day_stats = []
    for day in range(0, 7):
        current_day = datetime.date.today() - datetime.timedelta(days=7) + datetime.timedelta(days=day)
        not_found = True
        for result in total_count_last_seven_days:
            if result["registered_date"] == current_day:
                seven_day_stats.append({
                    "date_created": current_day.strftime("%d.%m.%Y"),
                    "total": result["total"]
                })
                not_found = False
                break
        
        if not_found:
            seven_day_stats.append({
                "date_created": current_day.strftime("%d.%m.%Y"),
                "total": 0
            })
            
    context = {"seven_day_stats":json.dumps(seven_day_stats)}
    return render(request, 'main/dashboard.html', context)


# @login_required(login_url='/login/')
# def customer_list(request):

#     context = {}
#     return render(request, 'main/customer_list.html', context)

@login_required(login_url='/login/')
def customer_view(request, id):
    client = m.Client.objects.filter(pk=id)
    client_remedial_detail = m.ClientDetailInfo.objects.filter(client=client.first())
    client_remedial_history = m.ClientMedicalHistory.objects.filter(detail_client_info=client_remedial_detail.first()).order_by("-date_created")
    
    client = client.values().first()
    client_remedial_detail = client_remedial_detail.values().first()

    
    client_info = {
        "id": client["id"],
        "first_name": client["first_name"],
        "last_name": client["last_name"],
        "health_insurance_number": str(client["health_insurance_number"]),
        "reference_number": str(client["reference_number"]),
        "email": client["email"],
        "DOB": client["DOB"],
        "phone_day": client["phone_day"],
        "phone_night": client["phone_night"],
        "address": client_remedial_detail["address"],
        "suburb": client_remedial_detail["suburb"],
        "state": client_remedial_detail["state"],
        "post_code": client_remedial_detail["post_code"],
        "occupation": client_remedial_detail["occupation"],
        "employer": client_remedial_detail["employer"],
        "primary_physician": client_remedial_detail["primary_physician"],

        "emergency_contact_name": client_remedial_detail["emergency_contact_name"],
        "emergency_contact_number": client_remedial_detail["emergency_contact_number"],
        "emergency_contact_relation": client_remedial_detail["emergency_contact_relation"],
        "hear_about_us": client_remedial_detail["hear_about_us"],
        "date_created": datetime.datetime.strftime(client["date_created"], "%d %b %Y %H:%M"),
    }

    history_container = []
    for history in client_remedial_history:
        history_container.append({
            "id": history.id,
            "medication": "YES" if history.medication else "N/A" if history.medication is None else "No",
            "medication_detail": history.medication_detail,

            
            "pregnant": "YES" if history.pregnant else "N/A" if history.pregnant is None else "No",
            "pregnant_time": history.pregnant_time,
            "pregnant_factor": history.pregnant_factor,

            "chronic_pain": "YES" if history.chronic_pain else "N/A" if history.chronic_pain is None else "No",
            "chronic_pain_detail": history.chronic_pain_detail,
            "chronic_pain_worse": history.chronic_pain_worse,
            "chronic_pain_better": history.chronic_pain_better,

            "orthopedic_injuries": "YES" if history.orthopedic_injuries else "N/A" if history.orthopedic_injuries is None else "No",
            "orthopedic_injuries_detail": history.orthopedic_injuries_detail,

            "conditions": f"{history.conditions}",
            "conditions_detail": history.conditions_detail,

            "professional_massage": "YES" if history.professional_massage else "N/A" if history.professional_massage is None else "No",

            "massage_type": f"{history.massage_type}",
            "massage_type_other": history.massage_type_other,

            "pressure_preference": f"{history.pressure_preference}",

            "allergies": "YES" if history.allergies else "N/A" if history.allergies is None else "No",
            "allergies_detail": history.allergies_detail,
            
            "no_massage_area": "YES" if history.no_massage_area else "N/A" if history.no_massage_area is None else "No",
            "no_massage_area_detail": history.no_massage_area_detail,

            "area_of_soreness":history.area_of_soreness.url if history.area_of_soreness else "",
            "reason_of_visit": history.reason_of_visit,
            
            "additional_comments": history.additional_comments,
            "receipt_image": history.receipt_image.url if history.receipt_image else "",
            "remedial_treatment_plan": history.remedial_treatment_plan if history.remedial_treatment_plan else "",
            "signature": history.signature.url if history.signature else "",
            "date_created": datetime.datetime.strftime(history.date_created, "%d %b %Y %H:%M")
        })

    context = {
        "client_info": client_info,
        "client_remedial_history": json.dumps(history_container)
    }
    return render(request, 'main/client_view.html', context)


@login_required(login_url='/login/')
def customer_edit(request, id):
    client = m.Client.objects.get(pk=id)
    client_remedial_detail = m.ClientDetailInfo.objects.get(client=client)
    if request.method =="POST":
        client_form = f.CustomerCheckInForm(request.POST, instance=client)
        remedial_form = f.DetailedClientForm(request.POST, instance=client_remedial_detail)

        if client_form.is_valid() and remedial_form.is_valid():

            client_form.save()
            remedial_form.save()


            return redirect("client_view", id=id)


    else:
        client_form = f.CustomerCheckInForm(instance=client) 
        remedial_form = f.DetailedClientForm(instance=client_remedial_detail)
    

    
    context = {
        "client_form": client_form,
        "remedial_form": remedial_form,
        "id": id
    }
    return render(request, 'main/client_edit.html', context)


@login_required(login_url='/login/')
def check_in(request):
    jwt_token = jwt.encode(
        {
            "time": datetime.datetime.now().strftime("%H:%M:S"),
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30)
        }, 
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    context = {"token":jwt_token}
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

def remedial_check_in_form(request,token):
    try:
        jwt.decode(token, settings.SECRET_KEY, "HS256")
    except jwt.ExpiredSignatureError as e:
        print(e)
        return redirect("error_page", title="Paradise Massage")

    if request.method =="POST":
       
        client_form = f.CustomerCheckInForm(request.POST)
        detailed_client_form = f.DetailedClientForm(request.POST)
        client_medical_history_form = f.ClientMedicalHistoryForm(request.POST, request.FILES)

      
        if client_form.is_valid() and detailed_client_form.is_valid() and client_medical_history_form.is_valid():

            client = client_form.save()
            detail_client_info = detailed_client_form.save(commit=False)
            client_medical_history = client_medical_history_form.save(commit=False)
            
            detail_client_info.client = client
            detail_client_info.save()

            
            client_medical_history.detail_client_info = detail_client_info

            client_medical_history.area_of_soreness = CustomMemoryFile(client_medical_history.area_of_soreness.name).memory_file
            client_medical_history.signature = CustomMemoryFile(client_medical_history.signature.name).memory_file
            
            client_medical_history.save()
       

            return redirect("form_submitted", title="Client Intake Form")


    else:
        client_form = f.CustomerCheckInForm() 
        detailed_client_form = f.DetailedClientForm()
        client_medical_history_form = f.ClientMedicalHistoryForm()
    
    # print(request.POST)
    
    context = {
        "client_form": client_form,
        "detailed_client_form": detailed_client_form,
        "client_medical_history_form":client_medical_history_form
    }
    return render(request, 'form/remedial_check_in_form.html', context)


def existing_remedial_check_in_form(request, token):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, "HS256")
        id = data["id"]
    except jwt.ExpiredSignatureError as e:
        print(e)
        return redirect("error_page", title="Paradise Massage")
    

    if request.method =="POST":

        

        
       
        remedial_history_form = f.ClientMedicalHistoryForm(request.POST, request.FILES)



        if remedial_history_form.is_valid():
            remedial_client_history = remedial_history_form.save(commit=False)
            
            remedial_client_history.detail_client_info = m.ClientDetailInfo.objects.get(id=id)
            remedial_client_history.area_of_soreness = CustomMemoryFile(remedial_client_history.area_of_soreness.name).memory_file
            remedial_client_history.signature = CustomMemoryFile(remedial_client_history.signature.name).memory_file
            remedial_client_history.save()

            return redirect("form_submitted", title="Client Intake Form")
        

    else:
       
        remedial_history_form = f.ClientMedicalHistoryForm()
    

    context = {
        "remedial_history_form":remedial_history_form
    }
    return render(request, 'form/remedial_check_in_form.html', context)

def form_submitted(request, title):
    context = {"title":title}
    return render(request, 'form/form_submitted.html', context)

def error_page(request, title):
    context = {"title":title}
    return render(request, 'form/error_page.html', context)


def upload_receipt(request):
    if request.method == "POST":
        if request.FILES.get("image", None) is not None:
            remedial_history_id = request.POST.get("id")
            img = request.FILES["image"]
            try:
                i = Image.open(img)
                thumb_io = BytesIO()
                i.save(thumb_io, format='JPEG', quality=80)
                in_memory_uploaded_file = InMemoryUploadedFile(thumb_io, None, 'remedial_receipt_{id}.jpg'.format(id=remedial_history_id), 'image/jpeg', thumb_io.tell(), None)
                
                remedial_history = m.ClientMedicalHistory.objects.get(pk=remedial_history_id)

                if remedial_history.receipt_image:
                    remedial_history.receipt_image.delete()
                    
                remedial_history.receipt_image = in_memory_uploaded_file
                remedial_history.save()

              
                response = HttpResponse()
                response['Content-Type'] = 'application/json'
                return response

            except Exception as e:
                print(e, flush=True)
                context = {
                    "error": e
                }
                response = HttpResponse(json.dumps(context), status=400)
                response['Content-Type'] = 'application/json'
                return response

            
    response = HttpResponse(status=400)
    response['Content-Type'] = 'application/json'
    return response


def get_treatment_plan_note(request):

    if request.method == "GET":
        try:
            id = request.GET.get("id")
            treatment_plan_note = m.ClientMedicalHistory.objects.get(id=id).remedial_treatment_plan
            
            context = {
                "note": treatment_plan_note
            }
            response = HttpResponse(json.dumps(context))
            response['Content-Type'] = 'application/json'
            return response

        except Exception as e:
            print(e)
            context = {
                "note": ""
            }
            response = HttpResponse(json.dumps(context), status=200)
            response['Content-Type'] = 'application/json'
            return response   
      
  
    response = HttpResponse(status=400)
    response['Content-Type'] = 'application/json'
    return response   

def set_treatment_plan_note(request):

    if request.method == "POST":
        try:
            id = request.POST.get("id")
            note = request.POST.get("note")
            remedial_history = m.ClientMedicalHistory.objects.get(id=id)
            remedial_history.remedial_treatment_plan = note
            remedial_history.save()
            response = HttpResponse()
            response['Content-Type'] = 'application/json'
            return response

        except Exception as e:
            print(e)
            response = HttpResponse(status=400)
            response['Content-Type'] = 'application/json'
            return response   
      
  
    response = HttpResponse(status=400)
    response['Content-Type'] = 'application/json'
    return response  

class ClientListView(ListView):
    model = m.Client
    template_name = 'main/client_list.html'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_json = []
        for client in context["object_list"]:
            jwt_token = jwt.encode(
                {
                    "id": client.clientdetailinfo_set.all()[0].id, 
                    "time": datetime.datetime.now().strftime("%H:%M:S"),
                    "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30)
                }, 
                settings.SECRET_KEY,
                algorithm="HS256"
            )

            client_json.append({
                "id": client.id,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "health_insurance_number": str(client.health_insurance_number),
                "reference_number": str(client.reference_number),
                "date_created": datetime.datetime.strftime(client.date_created, "%d %b %Y %H:%M"),
                "token": jwt_token
            })
        context["client_json"] = json.dumps(client_json)
        
        paginator = context["page_obj"]

        start_page, end_page = self._get_start_end_page(paginator.paginator.num_pages, paginator.number)
        context["paginator_range"] = range(start_page, end_page + 1)
        context["filter"] = self.request.GET.get('filter', '')
        
        return context

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):        
        return super(ClientListView, self).dispatch(request, *args, **kwargs)
    
    
    def get_queryset(self, **kwargs):
        filter_val = self.request.GET.get('filter', '')
        qs = super().get_queryset(**kwargs)
        return qs.filter(
            Q(first_name__icontains=filter_val) | 
            Q(last_name__icontains=filter_val) | 
            Q(phone_day__icontains=filter_val) | 
            Q(phone_night__icontains=filter_val) | 
            Q(health_insurance_number__icontains=filter_val))\
            .order_by("-date_created")
    


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


def csrf_failure(request, reason=""):
    context = {'message': 'Your session has expired.'}
    return render(request, 'main/csrf_failure.html', context)