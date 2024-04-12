from django.shortcuts import render,redirect
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import SignUpForm,TaskForm
from datetime import date, timedelta
from todoapp.models import Task
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpRequest
import random
# Create your views here.


def generate_random_number(num_digits):
    min_value = 10 ** (num_digits - 1)
    max_value = (10 ** num_digits) - 1
    return random.randint(min_value, max_value)

class CustomLoginView(LoginView):
    template_name = 'todoapp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def  get_success_url(self):
        return reverse_lazy('tasks')

class VerificationView(View):
    def get(self, request):
        return render(request, 'todoapp/verify.html')  
    def post(self, request):
        verification_data = request.POST.dict()
        secret_code = verification_data.get("secret_code")
        print(secret_code)

        verification_code = request.session.get('verification_code')

        if(verification_code == secret_code):
            return HttpResponse("Codes match")  
        return HttpResponse("Codes do not match")  


class SignUpForm(CreateView):
    template_name ="todoapp/register.html"
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self,form):
        user = form.save()

        verification_code = self.request.session.get('verification_code')
        
        secret_code = generate_random_number(6)
        verification_code = str(secret_code)
        self.request.session['verification_code'] = verification_code

        subject = 'Todo App: Group 1 app'
        message = "Dear " +user.username +", you have registered successfully. Click http://127.0.0.1:8000/verify-account?id=" + verification_code + " to verify your account!"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['deannahbeb@gmail.com','jovinkyomugaso@gmail.com', user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        if user is not None:
            login(self.request,user)
        return super(SignUpForm, self).form_valid(form)
    
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(SignUpForm,self).get(*args, **kwargs)    


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name='tasks'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(
                tittle__startswith=search_input)
                 
        context['search_input'] = search_input
        return context
        
class DeleteTasksView(View):
    def get(self, request):
        cutoff_date = created + timedelta(days=7)  # set cutoff date to 7 days from when task was created
        tasks_to_delete = Task.objects.filter(due_date__gt=cutoff_date)  # find all tasks with due dates after cutoff
        tasks_to_delete.delete()  # delete tasks from database
        return render(request, 'delete_tasks.html')     
    
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name= 'task'
    template_name= 'todoapp/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model= Task
    fields = ['tittle','discription','complete','due_date','due_time'] 
    success_url = reverse_lazy('tasks')
    #form_class = TaskForm
    template_name = 'todoapp/task_form.html'

    def form_valid(self,form):
        form.instance.user = self.request.user
        task = form.save(commit=False)
        task.owner = self.request.user
        task.save()
        return super().form_valid(form) 
   
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model= Task
    fields = ['tittle','discription','complete','due_date','due_time']
    success_url = reverse_lazy('tasks')
    #form_class = TaskForm
    template_name = 'todoapp/task_form.html' 
       
class DeleteView(LoginRequiredMixin,DeleteView):
    model= Task
    context_object_name='task'
    success_url = reverse_lazy('tasks') 



    
