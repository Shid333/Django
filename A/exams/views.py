from datetime import timedelta, datetime
from django.contrib import messages
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
		if not request.user.is_instructor:
			messages.error(request, "You do not have permission to create exams.", 'danger')
			return redirect('home:home')
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		if not request.user.is_instructor:
			messages.error(request, "You do not have permission to create exams.", 'danger')
			return redirect('home:home')
		form = self.form_class(request.POST)
		question_form = QuestionForm(request.POST)
		if form.is_valid():
			start_date_str = form.cleaned_data['start_date'].isoformat()
			exam = Exams(
				creator=request.user,
				name=form.cleaned_data['name'],
				duration=form.cleaned_data['duration'],
				start_date=form.cleaned_data['start_date'],
			)
			exam.save()

			request.session['exam_id'] = exam.id  # Store exam_id instead of exam_details
			request.session['exam_name'] = form.cleaned_data['name']
			request.session['exam_duration'] = str(form.cleaned_data['duration'])
			request.session['exam_start_date'] = start_date_str

			return redirect('exams:create_questions')
		return render(request, self.template_name, {'form': form})


# the questions of the exam
class CreateExamQuestionView(LoginRequiredMixin, View):
	template_name = 'exams/create_exam_questions.html'  # Create this template for handling questions

	def get(self, request, *args, **kwargs):
		# Retrieve exam details from the session
		exam_details = request.session.get('exam_details', {})
		if not exam_details:
			return redirect('exams:create_exams')

		question_form = QuestionForm()
		return render(request, self.template_name, {'exam_details': exam_details, 'question_form': question_form})

	def post(self, request, *args, **kwargs):
		question_form = QuestionForm(request.POST)

		if question_form.is_valid():
			# Get or initialize the list of questions from the session
			questions = request.session.get('questions', [])

			current_question = {
				'question_text': question_form.cleaned_data['question_text'],
				'options': [
					question_form.cleaned_data['option1'],
					question_form.cleaned_data['option2'],
					question_form.cleaned_data['option3'],
					question_form.cleaned_data['option4'],
				],
				'correct_answers': question_form.cleaned_data['correct_answers'],
			}
			questions.append(current_question)
			request.session['questions'] = questions

			# Check if the instructor wants to add more questions or finish
			if 'finish' in request.POST:
				# If finished, save the exam details and questions to the database
				exam_details = request.session.pop('exam_details', None)
				if exam_details:
					if exam_details:
						exam_details['duration'] = datetime.strptime(exam_details['duration'], '%H:%M:%S').time()
						exam = Exams.objects.create(
							name=exam_details['name'],
							duration=timedelta(hours=exam_details['duration'].hour, minutes=exam_details['duration'].minute, seconds=exam_details['duration'].second),
							start_date=exam_details['start_date'],
							creator=request.user,
						)
					exam_questions = []
					for q in questions:
						question = exam.questions.create(
							question_text=q['question_text'],
							correct_answers=q['correct_answers'],
						)
						question.options.set(q['options'])

					# Clear the session data
					del request.session['questions']

					return redirect('exam-list')  # Redirect to the exam list page

			else:
				# If not finished, clear the current question form
				question_form = QuestionForm()

		return render(request, self.template_name,{'exam_details': request.session['exam_details'], 'question_form': question_form})


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
