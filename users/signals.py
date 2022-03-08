from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings


def createprofile(sender,instance,created,**kwargs):
    userobj = instance
    if created:
        profile = Profile.objects.create(
            user = userobj,
            name = userobj.username,
            email = userobj.email
        )
        print('profile is created for this user')

        subject = "welcome to developers web application"
        message = "Thank you for joining us"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        ) 


def deleteuser(sender,instance,**kwargs):
    profile = instance
    userobj = profile.user
    userobj.delete()
    print('user is also deleted')

def updateuser(sender,instance,created,**kwargs):
    if created == False:
        profile = instance
        user = profile.user
        user.first_name = profile.name
        user.email = profile.email
        user.username = profile.username
        user.save()
        print('user record updated')

post_save.connect(updateuser,sender=Profile)
post_save.connect(createprofile,sender=User)
post_delete.connect(deleteuser,sender=Profile)