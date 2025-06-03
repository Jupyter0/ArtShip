from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def auction(request):
    template = loader.get_template('auction.html')
    return HttpResponse(template.render())