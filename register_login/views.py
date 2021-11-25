from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def signup(request):
    context = {}
    form = UserCreationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("index")

    context.update({
        "form": form,
        "title": "Signup",
    })
    return render(request, 'register_login/signup.html', context)


def signin(request):
    context = {}
    form = AuthenticationForm(request, data=request.POST)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")

    context.update({
        "form": form,
        "title": "Signin",
    })
    return render(request, "register_login/signin.html", context)

