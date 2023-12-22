from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


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


class Test(models.Model):
	instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
	assigned_students = models.ManyToManyField(Student)
	#start_time = models.DateTimeField()
	#end_time = models.DateTimeField()

