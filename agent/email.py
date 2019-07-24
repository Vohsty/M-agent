from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(name,receiver,tenant):
    # Creating message subject and sender
    subject = 'Welcome to M-agent'
    sender = 'alvinmichoma@gmail.com'
    first_name=tenant.first_name
    building_name = tenant.house_name.building.building_name
    house_name = tenant.house_name.name

    #passing in the context vairables
    text_content = render_to_string('emails/passemails.txt',{"first_name": first_name, "building_name":building_name, "house_name":house_name})
    html_content = render_to_string('emails/passemails.html',{"first_name": first_name, "building_name":building_name, "house_name":house_name})


    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()