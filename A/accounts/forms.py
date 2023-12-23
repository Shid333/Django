from django import forms
from .models import User, Question, AnswerOption
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'phone_number', 'full_name', 'role')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
			raise ValidationError('passwords don\'t match')
		return cd['password2']

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField(help_text='you can change password using <a href=\'../password/\'>this form</a>')

	class Meta:
		model = User
		fields = ('email', 'phone_number', 'full_name', 'password', 'last_login', 'role')


class UserRegistrationForm(forms.Form):
	ROLE_CHOICES = [('Student', 'Student'), ('Instructor', 'Instructor')]

	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
	full_name = forms.CharField(label='full name', widget=forms.TextInput(attrs={'class': 'form-control'}))
	role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
	phone_number = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['text', 'option1', 'option2', 'option3', 'option4', 'correct_answers']

	correct_answers = forms.ModelMultipleChoiceField(
		queryset=Question.objects.none(),
		widget=forms.CheckboxSelectMultiple,
		required=False)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['correct_answers'].queryset = AnswerOption.objects.filter(question=self.instance)



