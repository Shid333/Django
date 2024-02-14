from django.db import models
from accounts.models import User
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from datetime import timedelta


class DurationAwareJSONEncoder(DjangoJSONEncoder):
	def default(self, obj):
		if isinstance(obj, models.DurationField):
			return str(obj)
		return super().default(obj)


class Exams(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_exams')
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	duration = models.DurationField()
	start_date = models.DateTimeField()
	questions = models.JSONField(default=list)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.questions = json.dumps(self.questions, cls=DurationAwareJSONEncoder)
		super().save(*args, **kwargs)


class StudentsOnExams(models.Model):
	exam_id = models.ForeignKey(Exams, on_delete=models.CASCADE)
	student = models.ForeignKey(User, on_delete=models.CASCADE)
	score = models.IntegerField(default=0)
	is_done = models.BooleanField(default=False)
	done_date = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"{self.exam_id.name} - {self.student.name}"

	def save(self, *args, **kwargs):
		if self.is_done and not self.done_date:
			# set done_date only if the exam is done and done_date is not already set
			self.done_date = timezone.now()
		super().save(*args, **kwargs)
