from django.db import models

class EmailData(models.Model):

	email_address = models.CharField(max_length = 150)
	first_name = models.CharField(max_length = 50)
	last_name = models.CharField(max_length = 50)
	hard_bounces = models.IntegerField()
	active = models.BooleanField(default = True)

	class Meta:
		ordering = ["email_address"]
		verbose_name_plural = "Email Data"

	@classmethod
	def check_if_exists(cls, email):
		objs = cls.objects.filter(email_address = email)
		if objs.count() > 0:
			return True
		else:
			return False

	def add_hard_bounce(self):
		self.hard_bounces = self.hard_bounces + 1
		if self.hard_bounces >= 3:
			self.active = False
		self.save()

class CleanedEmails(models.Model):

	'''
	Stores and rechecks cleaned emails.
	'''

	email_address = models.CharField(max_length = 150)
	mailchimp_bounces = models.IntegerField(default = 0)
	mandrill_bounces = models.IntegerField(default = 0)
	first_name = models.CharField(max_length = 100, null = True)
	last_name = models.CharField(max_length = 100, null = True)
	active = active = models.BooleanField(default = True)

	class Meta:
		ordering = ["email_address"]
		verbose_name_plural = "CleanedEmails"

	@classmethod
	def check_if_exists(cls, email):
		objs = cls.objects.filter(email_address = email)
		if objs.count() > 0:
			return True
		else:
			return False

	def add_mailchimp_bounce(self):
		self.mailchimp_bounces = self.mailchimp_bounces + 1
		if self.mailchimp_bounces >= 3:
			self.active = False
		self.save()
		return True

	def add_mandrill_bounce(self):
		self.mandrill_bounces = self.mandrill_bounces + 1
		if self.mailchimp_bounces >= 2:
			return False
		self.save()
		return True