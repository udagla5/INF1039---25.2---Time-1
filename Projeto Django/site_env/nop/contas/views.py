from django.shortcuts import render

# Create your views here.
def cadastro1(request):
    return render(request, 'cadastro1.html')

def cadastro2(request):
    return render(request, 'cadastro2.html')