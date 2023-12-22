from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

	def create_user(self, phone_number, email, full_name, role, password):
		if not phone_number:
			raise ValueError('user must have phone number')

		if not email:
			raise ValueError('user must have email')

		if not full_name:
			raise ValueError('user must have full name')

		if not role:
			raise ValueError('user must have role')

		user = self.model(phone_number=phone_number, email=self.normalize_email(email), full_name=full_name, role=role)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone_number, email, full_name, role, password):
		if not phone_number:
			raise ValueError('user must have phone number')
		if not email:
			raise ValueError('user must have email')
		if not full_name:
			raise ValueError('user must have full name')
		if not role:
			raise ValueError('user must have role')

		user = self.model(phone_number=phone_number, email=self.normalize_email(email), full_name=full_name)
		user.set_password(password)
		user.is_admin = True
		user.is_manager = True
		user.save(using=self._db)
		return user

	def create_instructor(self, phone_number, email, full_name, role, password):
		if not phone_number:
			raise ValueError('user must have phone number')
		if not email:
			raise ValueError('user must have email')
		if not full_name:
			raise ValueError('user must have full name')
		if not role:
			raise ValueError('user must have role')

		user = self.model(phone_number=phone_number, email=self.normalize_email(email), full_name=full_name)
		user.set_password(password)
		user.is_instructor = True
		if user.is_admin:
			user.role = 'manager'
		user.save(using=self._db)
		return user

	def create_student(self, phone_number, email, full_name, role, password):
		if not phone_number:
			raise ValueError('user must have phone number')
		if not email:
			raise ValueError('user must have email')
		if not full_name:
			raise ValueError('user must have full name')
		if not role:
			raise ValueError('user must have role')

		user = self.model(phone_number=phone_number, email=self.normalize_email(email), full_name=full_name)
		user.set_password(password)
		user.is_student = True
		if user.is_admin:
			user.role = 'manager'
		user.save(using=self._db)
		return user
