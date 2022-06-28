from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

# Create your views here.
def welcome(request):
    resturant = Resturant.objects.all()
    return render(request, 'index.html', {"resturant":resturant})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) 
        if form.is_valid():
            form.save() # Save user to Database
            username = form.cleaned_data.get('username') # Get the username that is submitted
            messages.success(request, f'Account created for {username}!') # Show sucess message when account is created
            return redirect('login') # Redirect user to Homepage
    else:
        form = UserRegisterForm()
    return render(request, 'users/registration.html', {'form': form})

@login_required
def profile(request):
    User_Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.user_profile)

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.user_profile) 
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.user_profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def upload(request):
    '''
    function to upload restaurant for display
    '''
    current_user = request.user
    if request.method == "POST":
        form = uploadform(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.save()
            return redirect('welcome')
    else:
        form = uploadform()
    context = {
        "form":form
    }

    return render(request,"resturant/upload.html",context)

def default_map(request):
    mapbox_access_token = 'pk.my_mapbox_access_token'
    return render(request, 'default.html', 
                  { 'mapbox_access_token': mapbox_access_token })