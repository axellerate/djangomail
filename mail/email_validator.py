'''

Initial lifecycle:

1) 	First, we fetch all of the cleaned email addresses from Mailchimp and storm them in CleanedEmails
   	every single night.
2) 	They each start their lifecycle with 1 hard bounce from Mailchimp's end and are marked as active.
   	Example of a new CleanedEmails object:
    	email: email@example.com
    	mailchimp_bounces: 1
    	mandrill_bounces: 0
    	attempts_to_contact: 0
    	active: True

Validation Stages:

1) 	Once we have cleaned emails in our database, we begin the stages of validation. First, we reattempt to 
	contact the address via Mandrill sending a email to the address and checking the webhook for a hard bounce (two times).

2)  If the Mandrill tests fail, we attempt to contact the email through Mailchimp by sending an email asking if they would
	like to resubscribe. If once again, this request hard bonces, we attempt one more time (two attempts).

3)  When the email object reaches 2 mandrill attempts and 3 mailchimp attempts with no response, we mark the email's 
	'active' property as 'False' and stop attempting to contact it. 

'''

from models import *
from django.core.mail import EmailMessage
import urllib, json
import mailchimp

from djrill.signals import webhook_event
from django.dispatch import receiver


# add our API Key
API_KEY = '88ef3b32f5e058551f87002407bd1fb8-us11'
# add our List ID
LIST_ID = '78cc803450'
# contact the API and authenticate our app
api = mailchimp.Mailchimp(API_KEY)


# hooks into the mandrill event and acts accordingly
@receiver(webhook_event)
def handle_bounce(sender, event_type, data, **kwargs):
    if event_type == 'hard_bounce' or event_type = 'soft_bounce':
        print "Message to %s bounced: %s" % (
            data['msg']['email'],
            data['msg']['bounce_description']
        )
        email = str(data['msg']['email'])
        email_obj = CleanedEmails.objects.get(email_address = email)
        email_obj.add_mandrill_bounce()
        return True
    return False


class EmailValidator(object):

	@classmethod
	def fetch_cleaned_emails(cls):
		'''
		Fetch and update the database of cleaned emails.
		'''

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
			check_if_exists = CleanedEmails.check_if_exists(member['email'])

			# if the email does not exist, add it to the database
			if check_if_exists == False:
				obj = CleanedEmails(email_address = member['email'], mailchimp_bounces = 1, mandrill_bounces = 0,
								first_name = member['first_name'], last_name = member['last_name']).save()

				return str(len(members)) + " email(s) have been added to the database."
		return "No emails have been added to the database"


	@classmethod
	def subscribe(cls, email_address):
		'''
		Subscribes an email address that has passed our tests back to the MailChimp List.
		'''
		email_obj = CleanedEmails.objects.get(email_address = email_address)
		data = api.lists.subscribe(LIST_ID, {'email': email_obj.email_address}, merge_vars={'FNAME':email_obj.first_name,
																							'LNAME':email_obj.last_name})
		print "Email address " + email_address + " has been successfully subscribed."
		return True


	@classmethod
	def resubscribe_cleaned(cls, email_address):
		'''
		Attempt to resubscribe cleaned addresses that have 2 mandrill attempts and under 3 mailchip attempts.
		Otherwise, mark the address as: active = False - thus cutting it lose.
		'''
		cleaned_addresses = EmailData.objects.filter(active = True, mandrill_bounces = 2)
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

	@classmethod
	def mandrill_test(cls, email_address):
		'''
		Attempts to contact the email VIA mandrill and acts on the results through 
		the webhook above (handle_bounce).
		'''
		email_obj = CleanedEmails.objects.get(email_address = email_address)
		if email_obj.mandrill_bounces == 2:
			print email_address + " has too may mandrill attempts to recontact it."
			return False
		msg = EmailMessage(subject="TEST!", from_email="support@example.com",
		                   to=[email_address])
		msg.send()
		return "Message sent to " + email_address
