from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class UserRegisterView(View):
	form_class = UserRegistrationForm
	template_name = 'accounts/register.html'

	def get(self, request):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			User.objects.create_student(cd['phone_number'], cd['email'], cd['full_name'], cd['password'])
			messages.success(request, 'you registered successfully :)', 'success')
			return redirect('home:home')
		return render(request, self.template_name, {'form': form})


class UserLoginView(View):
	form_class = UserLoginForm
	template_name = 'accounts/login.html'

	def get(self, request):
		form = self.form_class
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['phone_number'], password=cd['password'])
			if user is not None:
				login(request, user)
				messages.success(request, 'you logged in successfully', 'success')
				return redirect('home:home')
			messages.error(request, 'phone number or password is wrong', 'warning')
		return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.success(request, 'you logged out successfully', 'success')
		return redirect('home:home')


def get_user_role(request):
	user_role = getattr(request.user, 'role', 'student')
	return {'user_role': user_role}


