from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, Question, AnswerOption
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email', 'phone_number', 'is_admin', 'role')
	list_filter = ('is_admin',)

	fieldsets = (
		('Main', {'fields': ('email', 'phone_number', 'full_name', 'password')}),
		('Permissions', {'fields': ('is_admin', 'is_instructor', 'is_student', 'is_active', 'last_login')}),
		('Role', {'fields': ('role', )}),
	)

	add_fieldsets = (
		(None, {'fields': ('phone_number', 'email', 'full_name', 'password1', 'password2')}),
		('Role', {'fields': ('role',)}),
	)

	def save_model(self, request, user, form, change):
		# Set role based on the is_admin field
		if user.is_admin:
			user.role = User.MANAGER  # Set the role to MANAGER for users with is_admin set to True
		else:
			user.role = form.cleaned_data['role']  # Set the role based on the form data
		super().save_model(request, user, form, change)

	search_fields = ('email', 'full_name',)
	ordering = ('full_name',)
	filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(AnswerOption)
admin.site.register(Question)

