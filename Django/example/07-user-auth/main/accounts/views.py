from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

# Create your views here.

class AccountCreateView(CreateView):
    model = User
    template_name = 'accounts/form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:list')

class AccountsListView(ListView):
    model = User
    template_name = 'accounts/list.html'
    success_url = reverse_lazy('accounts:list')

class AccountDelete(DeleteView):
    model = User
    success_url = reverse_lazy('accounts:list')
