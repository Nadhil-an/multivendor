from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def detectUser(user):
    if user.role == 1:   # Vendor
        return 'vendorDashboard'
    elif user.role == 2:  # Customer
        return 'customerDashboard'
    else:
        return 'loginUser'

def send_verification_email(request,user,email_template,mail_subject):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template,{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.send()

def send_approve_mail(mail_template,context,mail_subject):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template,context)
    to_email = context['user'].email
    mail = EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.send()




