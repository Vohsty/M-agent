from django.shortcuts import render, redirect,get_object_or_404
from django.http  import HttpResponse, HttpResponseRedirect, Http404
import datetime as dt
from .models import *
from .forms import CreateUserForm, UploadPicForm, CreateBuildingForm,CreateHouseForm
from django_daraja.mpesa.core import MpesaClient
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .email import send_welcome_email, send_payment_email
import json

User = get_user_model()
# Create your views here.

@login_required(login_url='/accounts/login')
def home(request):
     user_type = get_object_or_404(User,pk=request.user.id)
     try:
          landlord= request.user.landlord
          buildings=landlord.buildings.all()
          return render(request, 'home.html',{"buildings":buildings})

     except Landlord.DoesNotExist:           
          user=request.user
          try:
               tenant=Tenant.objects.get(user=user)
               return render(request, 'pay.html',{'user':user} )
          except Tenant.DoesNotExist:
               return HttpResponse("You must be a Landlord or Tenant to access this page")


     except Exception as e:
          print(e)
          return "You must be a Landlord or Tenant to access this page"

          
@login_required(login_url='/accounts/login')
def pay_with_mpesa(request):
     cl = MpesaClient()
     tenant=request.user.tenant
     phone_number = tenant.phone_number
     rent=request.user.tenant.house_name.rent
     if rent and type(rent)==int:
          amount = rent
     account_reference = 'reference'
     transaction_desc = 'Description'
     callback_url = 'https://m-agent.herokuapp.com/magent_callback'
     response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
     print(response.text)
     return redirect('home')


@login_required(login_url='/accounts/login')
def welcome_email(request):
     tenant=request.user.tenant
     email= tenant.email
     name=tenant.first_name

@csrf_exempt
def stk_push_callback(request):
     try:
          data = request.body
          print("wacha ufala")
          json_data=json.loads(data.decode())
          # print(json_data)
          if json_data["Body"]["stkCallback"]["ResultCode"]==0:
               phone=json_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]
               amount=json_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
               short_code=json_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
               time=json_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]
               print(phone,amount,short_code)
               phone_number=str(phone).replace("254","0")
               print(phone_number)
               tenant=Tenant.objects.get(phone_number=phone_number)
               transaction=Transactions(tenant=tenant,amount=amount,short_code=short_code)
               transaction.house=tenant.house_name
               transaction.meta=data.decode()
               transaction.save()
               send_payment_email(tenant,transaction)
          else:
               error=json_data["Body"]["stkCallback"]["ResultDesc"]
               print(error)

     except Tenant.DoesNotExist:
          print("Tenant does not exist")

     except Exception as e:
          print(e)

     return HttpResponse("success")

def create_user(request,house_id):
     form=CreateUserForm()
     error=False
     house=get_object_or_404(House,id=int(house_id))
     if request.method == 'POST':
          form=CreateUserForm(request.POST,request.FILES)
          
          if form.is_valid():
               print("valid")
               if Tenant.objects.filter(email=form.cleaned_data["email"] or User.objects.filter(username=form.cleaned_data["email"])):
                    error="User with email already exists"
               if Tenant.objects.filter(phone_number=form.cleaned_data['phone_number']).first():
                    error="User with this Phone Number already exists"
               user=User(username=form.cleaned_data["email"])
               

               user.save()

               tenant=form.save(commit=False)
               house.vacant= False
               tenant.house_name=house
               # tenant.my_house=house
               tenant.user=user
               house.save()
               tenant.save()
               
               otp=tenant.generate_otp_password()
               pin=tenant.create_pin()    
               url=request.build_absolute_uri("/accounts/login")
               tenant=user.tenant
               email = tenant.email
               name = tenant.first_name
               send_welcome_email(name,email,tenant,pin,otp,url)
              


               if error==False:
                    return redirect('home')
          else:
               house.vacant= True
               print(form.errors)
     return render(request, "registration.html",{"form":form,"error":error,"house_id":house_id})   



def user_profile(request,id):
     user=User.user_profile(id=id)
     return render(request,'user_profile.html',{"user":user})


def edit_user(request,id):
     form=UploadPicForm
     user=User.user_profile(id=id)
     if request.method == 'POST':
          form=UploadPicForm(request.POST)
          if form.is_valid():
               user = form.save()
               return redirect('view_tenant')
     return render(request,'edit_user.html',{"user":user})


def create_building(request):
     form=CreateBuildingForm()
     error=False
     land= get_object_or_404(Landlord,user=request.user.id)
     if request.method == 'POST':
          form=CreateBuildingForm(request.POST)
          if form.is_valid():
               if Building.objects.filter(building_name=form.cleaned_data['building_name']).first():
                    error="Building with similar name already exists"
               else:
                    building = form.save(commit=False)
                    building.owner=get_object_or_404(Landlord,user=request.user)
                    building.save()
                    return redirect('home')
     return render(request, "building_reg.html",{"form":form,"error":error})

     # def form_valid(self, form):
     #    form.instance.owner = self.request.user
     #    return super().form_valid(form)

def create_house(request):
     error=False
     landlord=request.user.landlord
     form=CreateHouseForm(landlord=landlord)
     if request.method == 'POST':
          form=CreateHouseForm(request.POST,landlord=landlord)
          if form.is_valid():
               print(form.cleaned_data['building'])
               if House.objects.filter(name=form.cleaned_data['name'],building=form.cleaned_data['building']).first():
                    error="Building with similar name already exists"
               else:
                    house = form.save()
                    return redirect('home')
     return render(request, "house_reg.html",{"form":form,"error":error})

@login_required(login_url='/accounts/login')
def view_houses(request, building_name):
     try:
        this_building = Building.objects.get(building_name=building_name)
     except Building.DoesNotExist:
        raise Http404("Invalid Building Name")
     this_house = House.objects.filter( building=this_building)
     return render(request, 'users.html',{'this_house':this_house,'this_building':this_building})


@login_required(login_url='/accounts/login')
def view_tenant(request, house_id):
     # try:
     house=House.objects.get(id=house_id)
     tenant=house.occupant
     if not tenant:
          return Http404("This house is vacant")             
     return render(request, 'user_profile.html',{"tenant":tenant} )
     # except Exception e:
     #      return HttpResponse("Error occured")

