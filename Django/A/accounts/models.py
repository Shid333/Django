from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.contrib.auth import get_user_model


class User(AbstractBaseUser):
	email = models.EmailField(max_length=255, unique=True)
	phone_number = models.CharField(max_length=11, unique=True)
	full_name = models.CharField(max_length=30)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	STUDENT = 'student'
	INSTRUCTOR = 'instructor'
	MANAGER = 'manager'

	ROLE_CHOICES = [('Student', 'Student'), ('Instructor', 'Instructor'), ('Manager', 'Manager'), ]
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)

	# role flags
	is_student = models.BooleanField(default=False)
	is_instructor = models.BooleanField(default=False)
	is_manager = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELDS = ['email', 'full_name']

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin

	def save(self, *args, **kwargs):
		if not self.id:
			if self.role == self.STUDENT:
				self.is_student = True
			elif self.role == self.INSTRUCTOR:
				self.is_instructor = True
			elif self.role == self.MANAGER:
				self.is_manager = True
		super(User, self).save(*args, **kwargs)


class Manager(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)


class Instructor(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)


class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)


class AnswerOption(models.Model):
	text = models.CharField(max_length=255)

	def __str__(self):
		return self.text


class Question(models.Model):
	text = models.TextField()
	option1 = models.CharField(max_length=255)
	option2 = models.CharField(max_length=255)
	option3 = models.CharField(max_length=255)
	option4 = models.CharField(max_length=255)
	correct_answers = models.ManyToManyField(AnswerOption)


class ExamSubmission(models.Model):
	student = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey('Question', on_delete=models.CASCADE)
	selected_answers = models.ManyToManyField('AnswerOption')

	def evaluate_submission(self):
		# Get the correct answers for the question
		correct_answers = self.question.correct_answers.all()

		# Compare the selected answers with the correct answers
		is_correct = set(self.selected_answers.all()) == set(correct_answers)

		return is_correct








