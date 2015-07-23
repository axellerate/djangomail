from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import View
from models import *
from django.core.mail import EmailMessage
import urllib, json
import mailchimp

API_KEY = '88ef3b32f5e058551f87002407bd1fb8-us11'
LIST_ID = '78cc803450'
api = mailchimp.Mailchimp(API_KEY)

from djrill.signals import webhook_event
from django.dispatch import receiver

@receiver(webhook_event)
def handle_bounce(sender, event_type, data, **kwargs):
    if event_type == 'hard_bounce' or event_type == 'soft_bounce':
        print "Message to %s bounced: %s" % (
            data['msg']['email'],
            data['msg']['bounce_description']
        )


class Subscribe(View):

	def get(self, request, *args, **kwargs):
		email = request.GET.get('email')
		data = api.lists.subscribe(LIST_ID, {'email': email}, merge_vars={'FNAME':"Kris",'LNAME':"V"})
		json_data = data['data'][0]
		return HttpResponse(json_data)

class Unsubscribe(View):

	def get(self, request, *args, **kwargs):
		email = request.GET.get('email')
		data = api.lists.unsubscribe(LIST_ID, {'email': email}, 
			                                   delete_member = True,
			                                   send_notify = True)
		json_data = data['data'][0]
		return HttpResponse(json_data)

class Subscribed(View):

	def get(self, request, *args, **kwargs):
		email = request.GET.get('email')
		data = api.lists.members(LIST_ID, status = "subscribed")
		json_data = data['data'][0]
		return HttpResponse(json_data)

class UpdateCleaned(View):

	'''
	Iterates through the 'cleaned' email addresses on MailChimp and updates the 
	bounce count on our system.
	'''

	def get(self, request, *args, **kwargs):
		data = api.lists.members(LIST_ID, status = "cleaned")
		json_data = data['data']
		members = []
		for item in json_data:
			temp_dict = {}
			temp_dict.update({'email': item['email']})
			temp_dict.update({'first_name': item['merges']['FNAME']})
			temp_dict.update({'last_name': item['merges']['LNAME']})
			members.append(temp_dict)
		# first, we check if the email exists

		for member in members:
			check_if_exists = EmailData.check_if_exists(member['email'])

			# if the email does not exist, add it to the database
			if check_if_exists == False:
				obj = EmailData(email_address = member['email'], hard_bounces = 0,
								first_name = member['first_name'], last_name = member['last_name']).save()
			# if the email already exists, add a hard bounce to the count
			else:
				obj = EmailData.objects.get(email_address = member['email'])
				obj.add_hard_bounce()

		return HttpResponse(members)


class ResubscribeCleaned(View):

	def mandrill_email_check(self):
		msg = EmailMessage(subject="TEST!", from_email="support@facebook.com",
		                   to=["axellerateeuiofj@gmail.com", "krisvdev@gmail.com"])
		msg.send()

	def get(self, request, *args, **kwargs):
		self.mandrill_email_check()
		cleaned_addresses = EmailData.objects.filter(active = True)
		for email_address in cleaned_addresses:
			try:
				# delete the address from MailChimp
				api.lists.unsubscribe(LIST_ID, {'email': email_address.email_address}, 
				                                   		delete_member = True,
				                                   		send_notify = True)
			except:
				# resubscribe the address
				data = api.lists.subscribe(LIST_ID, {'email': email_address.email_address}, 
													merge_vars={'FNAME':email_address.first_name,
																'LNAME':email_address.last_name})

		return HttpResponse(cleaned_addresses.count())
