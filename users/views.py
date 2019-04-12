from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


def register(request):
	if request.method == 'GET':
		form = UserRegisterForm()
		return render(request, 'users/register.html',{'form':form})
	elif request.method == 'POST':
		input_data_form = UserRegisterForm(request.POST)
		if input_data_form.is_valid():
			user = input_data_form.save()
			username = input_data_form.cleaned_data.get('username')
			messages.success(request, 'Account created for {username}'.format(username=username))
		else:
			return render(request, 'users/register.html',{'form':input_data_form})
		return redirect('login')

@login_required
def profile(request):
	user_form = UserUpdateForm(instance=request.user)
	profile_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
	'user_form':user_form,
	'profile_form':profile_form,
	}

	if request.method == 'GET':
		return render(request, 'users/profile.html',context=context)
	elif request.method == 'POST':
		user_input = UserUpdateForm(request.POST, instance=request.user)
		profile_input = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		
		if user_input.is_valid() and profile_input.is_valid():
			user_input.save()
			profile_input.save()
			messages.success(request, 'Account updated!')
			return redirect('profile')
		else:
			return render(request, 'users/profile.html',context=context)

