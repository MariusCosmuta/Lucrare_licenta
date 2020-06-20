from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RegisterForm


# Create your views here.

def logout_request(request):
    logout(request)
    return redirect("/")



def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form": form})
