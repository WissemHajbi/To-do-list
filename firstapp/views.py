from django.shortcuts import render,redirect
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import goal
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class GoalList(LoginRequiredMixin, ListView):
    model = goal
    context_object_name = 'goals'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goals'] = context['goals'].filter(user=self.request.user)
        search_input=self.request.GET.get('search_area') or ''
        if search_input :
            context['goals'] = context['goals'].filter(title__startswith=search_input) 
        context['search_input'] = search_input
        return context

class GoalDetail(LoginRequiredMixin, DetailView):
    model = goal
    context_object_name = 'goal'
    template_name = 'firstapp/goal.html'
    
class GoalCreate(LoginRequiredMixin, CreateView):
    model = goal
    fields = ['title','description','done']
    success_url = reverse_lazy('goal_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(GoalCreate, self).form_valid(form) 

class GoalUpdate(UpdateView):
    model = goal
    fields = ['title','description','done'] 
    success_url = reverse_lazy('goal_list')
    
class GoalDelete(DeleteView):
    model = goal
    context_object_name = "goal"
    success_url = reverse_lazy('goal_list')

class Login(LoginView):
    template_name = 'firstapp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('goal_list')
    
class Register(FormView):
    template_name = 'firstapp/register.html'
    form_class = UserCreationForm
 
    def get_success_url(self):
        return reverse_lazy('goal_list')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            Login(self.request, user)
        return super(Register,self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('goal_list')
        return super(Register,self).get(*args, **kwargs)