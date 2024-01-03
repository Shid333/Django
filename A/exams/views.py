from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ExamsForm, QuestionForm
from django.utils import timezone
from .models import Exams
from accounts.models import User
from accounts.views import get_user_role


# the detail page of the exam
class CreateExamsView(LoginRequiredMixin, View):
	form_class = ExamsForm
	template_name = 'exams/create_exams.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		question_form = QuestionForm(request.POST)
		if form.is_valid():
			start_date_str = form.cleaned_data['start_date'].isoformat()
			request.session['exam_details'] = {
				'name': form.cleaned_data['name'],
				'duration': form.cleaned_data['duration'],
				'start_date': start_date_str,
			}
			return redirect('exams/create_questions')
		return render(request, self.template_name, {'form': form})


# the questions of the exam
class CreateExamQuestionView(LoginRequiredMixin, View):
	template_name = 'exams/create_exam_questions.html'  # Create this template for handling questions

	def get(self, request, *args, **kwargs):
		# Retrieve exam details from the session
		exam_details = request.session.get('exam_details', {})
		if not exam_details:
			return redirect('create_exams')  # Redirect back to the first step if details are not available

		question_form = QuestionForm()
		return render(request, self.template_name, {'exam_details': exam_details, 'question_form': question_form})

	def post(self, request, *args, **kwargs):
		question_form = QuestionForm(request.POST)

		if question_form.is_valid():
			# Get or initialize the list of questions from the session
			questions = request.session.get('questions', [])

			# Add the current question to the list
			questions.append({
				'question_text': question_form.cleaned_data['question_text'],
				'options': [
					question_form.cleaned_data['option1'],
					question_form.cleaned_data['option2'],
					question_form.cleaned_data['option3'],
					question_form.cleaned_data['option4'],
				],
				'correct_answers': question_form.cleaned_data['correct_answers'],
			})

			# Save the updated list back to the session
			request.session['questions'] = questions

			# Check if the instructor wants to add more questions or finish
			if 'finish' in request.POST:
				# If finished, save the exam details and questions to the database
				exam_details = request.session.pop('exam_details', None)
				if exam_details:
					exam = Exams.objects.create(
						name=exam_details['name'],
						duration=exam_details['duration'],
						start_date=exam_details['start_date'],
						creator=request.user,
					)
					exam.questions = questions
					exam.save()

					# Clear the session data
					del request.session['questions']

					return redirect('exam-list')  # Redirect to the exam list page

			else:
				# If not finished, clear the current question form
				question_form = QuestionForm()

		return render(request, self.template_name, {'exam_details': request.session['exam_details'], 'question_form': question_form})


class ExamsView(View):
	def get(self, request):
		return render(request, 'exams/exams.html')


class ViewExamsView(View):
	def get(self, request):
		return render(request, 'exams/view_exams.html')


class ShowExamsView(View):
	def get(self, request):
		user = request.user
		if user.user_role == 'instructor':
			pass
