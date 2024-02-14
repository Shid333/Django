from django.urls import path
from . import views


app_name = 'exams'
urlpatterns = [
	path('create_exams/', views.CreateExamsView.as_view(), name='create_exams'),
	path('create_questions', views.CreateExamQuestionView.as_view(), name='create_questions'),
	path('exams/', views.ExamsView.as_view(), name='exams'),
	path('show/', views.ShowExamsView.as_view(), name='show_exams'),
	path('view/', views.ViewExamsView.as_view(), name='view_exams'),
]