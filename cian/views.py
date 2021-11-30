from django.http import request, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView, ListView
from .forms import UrlForm
from .models import Image, Apartment
import os
import json


class IndexView(ListView, FormView):
    model = Apartment
    template_name = 'cian/index.html'
    success_url = reverse_lazy('home')
    context_object_name = 'apartments_list'
    form_class = UrlForm

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['images'] = Image.objects.all()
    #     return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)