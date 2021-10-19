from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,  login, logout
# Create your views here.
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse


    

    
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("learning_logs:topics"))
    return render(request, r"users\login.html")
    
    
    
def logout_view(request):
    logout(request)
    return render(request, "users\login.html", {
        "message": "Logged out"
    })   
    
def register(request):
    if request.method != "POST":
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            authentucated_user = authenticate(request, username = user.username, password = user.password)
            login(request, authentucated_user)
            return HttpResponseRedirect(reverse('learning_logs:Topics'))
            
            
            
    form = UserCreationForm()    
    return render(request, r"users\register.html",
    {"form": form}
    )
    
    
    