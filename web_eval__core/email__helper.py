import datetime
import random
import string
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from webEval.settings import HOST_URL

def send_validation_key (username, key):
    validation_key = ''.join([random.choice(string.letters + string.digits) for i in range(0, 32)])
    key.key = validation_key
    key.username = username
    key.expire_date = datetime.datetime.now() + datetime.timedelta(days=2)
    key.save()
    
    email_subject = 'Your webEval account confirmation'
    email_body = "Hello, and thanks for signing up for an webEval account!\n\nTo activate your account, click this link within 48 hours:\n\n%s%s\n\nIf you didn't register on this site, please ignore this mail." \
                % (HOST_URL,
                   reverse('webEval.web_eval__core.auth__controller.validate_user',
                   kwargs={'validation_key' : validation_key,
                           'user_name' : username.username}))
    email = EmailMessage(email_subject, email_body, to=[username.email])
    email.send()