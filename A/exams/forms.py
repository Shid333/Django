from django import forms
from .models import Exams
from django.contrib.admin import widgets
from accounts.models import User


class QuestionForm(forms.Form):
	question_text = forms.CharField(label='Question', max_length=255)
	option1 = forms.CharField(max_length=255)
	option2 = forms.CharField(max_length=255)
	option3 = forms.CharField(max_length=255)
	option4 = forms.CharField(max_length=255)
	correct_answers = forms.MultipleChoiceField(
		choices=[('option1', 'Option1'), ('option2', 'Option2'), ('option3', 'Option3'), ('option4', 'Option4')],
		widget=forms.CheckboxSelectMultiple)


class ExamsForm(forms.ModelForm):
	class Meta:
		model = Exams
		fields = ['name', 'duration', 'start_date']

	widgets = {
		'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
	}
	duration = forms.DurationField(widget=forms.TextInput(attrs={'placeholder': 'e.g., 2 hours, 30 minutes'}), help_text='Enter the duration in the format HH:MM:SS or use a user-friendly format like 2 hours, 30 minutes.')


class StudentSelectionForm(forms.ModelForm):
	students = forms.ModelMultipleChoiceField(queryset=User.objects.filter(role='student'), widget=forms.CheckboxSelectMultiple, )

	class Meta:
		model = Exams
		fields = ['students']
