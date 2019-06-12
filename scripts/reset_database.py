from EasyChatApp.models import *
from django.contrib.auth.hashers import make_password

import os

cmd = "rm db.sqlite3 EasyChatApp/migrations/00*"
os.system(cmd)

cmd = "python manage.py makemigrations"
os.system(cmd)

cmd = "python manage.py migrate"
os.system(cmd)

user = User.objects.create(username='admin', password=make_password(
    'adminadmin'), is_staff=True, is_superuser=True)

Config.objects.create()
Channel.objects.create(name='Web')
Channel.objects.create(name='GoogleHome')
Channel.objects.create(name='Alexa')
Channel.objects.create(name='WhatsApp')
Channel.objects.create(name='Android')

DefaultIntent.objects.create(intent_name="Hi",
                             variations="Hey, hello",
                             answer="Hi! How may I assist you?")

DefaultIntent.objects.create(intent_name="Helpful",
                             variations="thank you, good bot, awesome, amazing, fantastic, good work, fantabulous, excellent, wonderful, outstanding, superb, perfect, marvellous",
                             answer="Glad that you like my service! Hoping to serve you again.")

DefaultIntent.objects.create(intent_name="Unhelpful",
                             variations="worst, bad bot, not helpful, time waste, bad experience, horrible, miserable, pathetic",
                             answer="Glad that you like my service! Hoping to serve you again.")

DefaultIntent.objects.create(intent_name="contact customer care",
                             variations="please help me connect to your customer service, i want to talk to customer care, help me get in touch with customer service team, i want my issues to be resolved by customer care",
                             answer="Please visit http://allincall.in to connect with customer care")

DefaultIntent.objects.create(intent_name="bye",
                             variations="good bye",
                             answer="Thanks for using EasyChat. See you soon!")
