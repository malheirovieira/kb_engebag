from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def base_conhecimento(request):
    return render(request, 'base_conhecimento.html')