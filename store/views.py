from django.shortcuts import render
from django.views.generic import TemplateView

class StoreListView(TemplateView):
    template_name = 'cart.html'

