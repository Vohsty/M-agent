from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_welcome_email(name,receiver,tenant,pin,otp,url):
    # Creating message subject and sender
    subject = 'Welcome to M-agent'
    sender= settings.EMAIL_HOST_USER
    first_name=tenant.first_name
    building_name = tenant.house_name.building.building_name
    house_name = tenant.house_name.name
    pin=tenant.pin
    email=tenant.email
    otp=tenant.generate_otp_password()
    # url=request.build_absolute_uri("/accounts/login")

    #passing in the context vairables
    text_content = render_to_string('emails/passemails.txt',{"first_name": first_name, "building_name":building_name, "house_name":house_name, "pin":pin,"email":email,"otp":otp,"url":url})
    html_content = render_to_string('emails/passemails.html',{"first_name": first_name, "building_name":building_name, "house_name":house_name,"pin":pin,"email":email,"otp":otp,"url":url})


    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()


def send_payment_email(tenant,transaction):
    subject="Rent payment"
    amount=transaction.amount
    time=transaction.created_at.strftime("%Y-%m-%d %H:%M:%S")
    short_code=transaction.short_code
    email=tenant.email
    sender= settings.EMAIL_HOST_USER
    house=tenant.house_name
    text_content = render_to_string('emails/payment_email.txt',{"first_name": tenant.first_name, "house_name":house.name,"amount":amount,"short_code":short_code,"time":time})
    html_content = render_to_string('emails/payment_email.html',{"first_name": tenant.first_name, "house_name":house.name,"amount":amount,"short_code":short_code,"time":time})

    msg = EmailMultiAlternatives(subject,text_content,sender,[email])
    msg.attach_alternative(html_content,'text/html')
    msg.send()


