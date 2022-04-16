from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .models import Editor
from .forms import EditorEditForm

# Create your views here.

class EditorCreate(CreateView):
    model = Editor
    form_class = EditorEditForm
    template_name = 'editors/form.html'
    success_url = reverse_lazy('editors:list')

class EditorsList(ListView):
    model = Editor
    template_name = 'editors/list.html'
    success_url = reverse_lazy('editors:list')

class EditorUpdate(UpdateView):
    model = Editor
    form_class = EditorEditForm
    template_name = 'editors/form.html'
    success_url = reverse_lazy('editors:list')

class EditorDelete(DeleteView):
    model = Editor
    success_url = reverse_lazy('editors:list')
