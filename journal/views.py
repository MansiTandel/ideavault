from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CreateUserForm, LoginForm, IdeaPostForm, IdeaUpdateForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Idea, Profile

from django.core.mail import send_mail

from django.conf import settings

def home(request):
      
    return render(request,"index.html")

# - Register

def register(request):
    
    form = CreateUserForm()

    #form2 = UpdateProfileForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():

            current_user = form.save(commit=False)

            form.save()

            send_mail("Welcome to IdeaVault!","Congratulations, on creating your account!",
                      settings.DEFAULT_FROM_EMAIL,[current_user.email])

            # - Create a blank object for a single instance with a FK attached

            profile = Profile.objects.create(user=current_user)

            messages.success(request, "Your account was created!")
            return redirect('my-login')
        
    context = {'form':form}

    return render(request,'register.html',context)

# - Login

def my_login(request):

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request,"Successfully logged in")
                return redirect('dashboard')
            
    context = {'form' : form}
    return render(request,'my-login.html', context=context)

# - Dashboard
@login_required(login_url="my-login")
def dashboard(request):

    profile_pic = Profile.objects.get(user=request.user)

    context = {'profilePic':profile_pic}

    return render(request, 'profile/dashboard.html', context = context)



    return render(request,"profile/dashboard.html")

# - Post an Idea
@login_required(login_url="my-login")
def post_idea(request):
    form = IdeaPostForm()
    if request.method=='POST':
        form = IdeaPostForm(request.POST)

        if form.is_valid():
            idea = form.save(commit=False)
            idea.user = request.user
            idea.save()

            messages.success(request,"You just posted a new idea!")
            return redirect('my-ideas')
    context = {'form':form}
    return render(request,'profile/post-idea.html',context=context)

# 
@login_required(login_url="my-login")
def my_ideas(request):
    current_user = request.user.id
    idea = Idea.objects.all().filter(user=current_user)

    context = {'idea':idea}
    return render(request, 'profile/my-ideas.html',context= context)

@login_required(login_url="my-login")
def update_idea(request, pk):
    idea = Idea.objects.get(id=pk)
    form = IdeaUpdateForm(instance=idea)

    if request.method == 'POST':
        form = IdeaUpdateForm(request.POST, instance=idea)

        if form.is_valid():
            form.save()
            messages.success(request,"You just updated your idea")
            return redirect('my-ideas')
        
    context =  {'form':form}
    return render(request,'profile/update-idea.html',context=context)

# - Delete
@login_required(login_url="my-login")
def delete_idea(request, pk):
    idea = Idea.objects.get(id=pk)

    if request.method == 'POST':

        idea.delete()
        messages.success(request, "You just deleted your idea")
        return redirect('my-ideas')
    
    return render(request, 'profile/delete-idea.html')

# - profile management -update username, password
@login_required(login_url="my-login")
def profile_management(request):
    
    form = UpdateUserForm(instance=request.user)

    profile = Profile.objects.get(user=request.user)

    # - Profile form for Profile PICTURE
    form_2 = UpdateProfileForm(instance=profile)


    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        form_2 = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()    # if update is made, redirect to the dashboard
            messages.success(request, "Update- username/email was a success!")
            return redirect('dashboard')
        
        if form_2.is_valid():
            form_2.save()    # if update is made, redirect to the dashboard
            messages.success(request,"Your profile picture was successfully updated!")
            return redirect('dashboard')
        
        
    context =  {'form':form, 'form_2':form_2}
    return render(request,'profile/profile-management.html',context=context)

# - delete account
@login_required(login_url="my-login")
def delete_account(request):

    if request.method == 'POST':
        deleteUser = User.objects.get(username=request.user)
        # model's object->username->loggedin User

        deleteUser.delete()
        messages.success(request,"Your account has been deleted successfully!")
        return redirect('my-login')
    
    return render(request,'profile/delete-account.html')

# - user logout

def user_logout(request):
    auth.logout(request)
    messages.success(request,"Sucessfully logged out")
    return redirect("my-login")

