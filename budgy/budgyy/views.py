from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Sing
from .forms import SingForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
#line 7 was added just incase ;o

def home(request):
	if request.user.is_authenticated:
		form = SingForm(request.POST or None)
		if request.method == "POST":
			if form.is_valid():
				sing = form.save(commit=False)
				sing.user = request.user
				sing.save()
				messages.success(request,("your sing is now on budgy!🕊️... "))
				return redirect('home')

		sings = Sing.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"sings":sings, "form":form})
	else:
		sings = Sing.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"sings":sings})


def profile_list(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)
		return render(request, 'profile_list.html', {"profiles":profiles})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')
	
def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		sings = Sing.objects.filter(user_id=pk).order_by("-created_at")

		#follow unflollow logic part!!
		if request.method == "POST":
			current_user_profile = request.user.profile
			#form data
			action = request.POST['follow']
			#decisionn to follow unfollow
			if action  == "unfollow":
				current_user_profile.follows.remove(profile)
			elif action	== "follow":
				current_user_profile.follows.add(profile)

			#saving profile
			current_user_profile.save()


		return render(request, "profile.html", {"profile":profile, "sings":sings})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')
	

def login_user(request):	
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You have been logged in!! GO SINGING!!..."))
			return redirect('home')
		else:
			messages.success(request, ("There was a login error! Try again..."))
			return redirect('login')
	
	else:
		return render(request, "login.html", {})



def logout_user(request):
	logout(request)
	messages.success(request, ("logged out... Fly again back to this nest!"))
	return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']
			# last_name = form.cleaned_data['last_name']
			# email = form.cleaned_data['email']

			#logged in user
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have succesfully registered. Welcome!"))
			return redirect('home')

	return render(request, "register.html", {'form':form})

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		profile_user = Profile.objects.get(user__id=request.user.id)

		user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			login(request, current_user)
			messages.success(request, ("Your profile has been updated"))
			return redirect('home')

		return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})


	else:
		messages.success(request, ("OH! seems you are logged out, You must be logged in to view this page... "))
		return redirect('home')
	
