from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm
from .models import User
from django.contrib import messages


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
			User.objects.create_user(cd['phone_number'], cd['email'], cd['full_name'], cd['role'], cd['password'])
			messages.success(request, 'you registered successfully :)', 'success')
			return redirect('home:home')
		return render(request, self.template_name, {'form': form})

