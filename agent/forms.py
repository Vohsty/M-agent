from django import forms
from .models import User, Building, House, Tenant
# from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()
class CreateUserForm(forms.ModelForm):

    class Meta:
        model = Tenant
        # fields = ['first_name','last_name','email','id_number','house','house_number','phone_number','image','tenant','gender',]
        exclude=['user','tenant_hash','house_name']

class UploadPicForm(forms.ModelForm):

    class Meta:
        model = Tenant
       
        exclude=[]


class CreateBuildingForm(forms.ModelForm):

    class Meta:
        model = Building
        fields = ('building_name','building_location','street','plot_number',)

class CreateHouseForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        landlord=kwargs.pop("landlord",None)
        super(CreateHouseForm,self).__init__(*args,**kwargs)
        queryset=Building.objects.filter(owner=landlord)
        self.fields["building"]=forms.ModelChoiceField(queryset=queryset)

    class Meta:
        model = House
        fields = ('house_type','house_floor','name','vacant','building')       



   
