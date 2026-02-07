from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy # chaine bela matra view name bata url lincha

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin #user must be logged to access views
from django.contrib.auth.forms import UserCreationForm #default registration form
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Task
# Create your views here.

#two ways to write views:- Function-Based Views (FBVs) → def my_view(request): ...
#and Class-Based Views (CBVs) → class MyView(View): ...
#CBVs are used here to use it as a encapulation behaviour inorde to delete,create,update objects

class CustomLoginView(LoginView):
    template_name='base/login.html'
    fields = '__all__'
    redirect_authenticated_user= True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form): #registration form valid cha vani aafai naya user save garera log in garauncha
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs): #logged in user lai registration page access garna dedaina
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin,ListView):
    model= Task 
    context_object_name= 'tasks'  #listview le templates ma object_list phatauncha but yo garem vane tasks vanera phatauna milcha

    def get_context_data(self, **kwargs): #tasks belonging to loggedin user haru matra show garcha
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or '' #tasks haru search garna lai
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input       
        return context


class TaskDetail(LoginRequiredMixin,DetailView):
    model= Task 
    context_object_name= 'task'
    template_name='base/task.html'


class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form): #logged in user ma tasks set/save garcha
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)



class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks') #after successful action, django le user lai tasks vanne url defined in urls ma redirect garcha


class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name= 'task'
    success_url = reverse_lazy('tasks')

@login_required
def toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == "POST":
        task.complete = not task.complete
        task.save()
        return redirect('tasks')  # Go back to task list after toggle

    return render(request, 'base/task_toggle.html', {'task': task})