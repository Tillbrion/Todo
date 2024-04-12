from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models
from django.forms import ModelForm

class VerifyAccount(forms.ModelForm):
    secret_code = forms.CharField(widget = forms.Textarea(attrs={'placeholder': 'Enter Verification Code'}))
    

class SignUpForm(UserCreationForm):
    email= forms.EmailField(max_length=254,required=True)

    class Meta:
        model = User
        fields = ('username','email','password1','password2')
        
        
class TaskForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))    
    due_time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}))  
    

    class Meta:
        model = models.Task
        fields = ['tittle','discription','complete','due_date','due_time']
        
    def clean_tittle(self):
        tittle = self.cleaned_data['tittle']
        if tittle is None:
            raise forms.ValidationError("Task cannot be empty")
            return tittle   


    
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.fields['due_date'].widget.input_type='date'
    #     self.fields['time'].widget.input_type='time'






