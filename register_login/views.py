from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from register_login.forms import UpdateForm
from django.contrib.auth import logout as logoutuser


def signup(request):
    context = {}
    form = UserCreationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)

            # After successful signup redirect the user to profile update page
            return redirect("update-profile")

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

            # After successful signin redirect the user to index page
            if user is not None:
                login(request, user)
                return redirect("index")

    context.update({
        "form": form,
        "title": "Signin",
    })
    return render(request, "register_login/signin.html", context)

@login_required
def update_profile(request):
    context = {}

    # Retrieve authenticated user
    user = request.user
    form = UpdateForm(request.POST, request.FILES)

    if request.method == "POST":
        if form.is_valid():
            update_profile = form.save(commit=False)
            update_profile.user = user
            update_profile.save()

            # After successful profile updation redirect the user to index page
            return redirect("index")

    context.update({
        "form": form,
        "title": "Update Profile",
    })
    return render(request, "register_login/update_profile.html", context)


@login_required
def logout(request):
    logoutuser(request)
    return redirect("index")