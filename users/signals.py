from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

# example
@receiver(post_save, sender=Profile)
def profileUpdated(sender, instance, created, **kwargs):
    print("Profile Saved!")
    print(f"Instance: {instance}")
    print(f"CREATED: {created}")

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    print("Deleting user...")


# def profileUpdated(sender, instance, created, **kwargs):
#     print("Profile Saved!")
#     print(f"Instance: {instance}")
#     print(f"CREATED: {created}")

# def deleteUser(sender, instance, **kwargs):
#     print("Deleting user...")
    
# post_save.connect(profileUpdated, sender=Profile)
# post_delete.connect(deleteUser, sender=Profile)

def createProfile(sender, instance, created, **kwargs):
    print("Profile signal triggered")
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
            )
        subject = "Welcome to DevSearch"
        message = "We are glad you are here!"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )

def updateProfile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
        print("ok")

def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user # Profile被刪除時，User也被刪除
        user.delete()
        print("Deleting user...")
    except:
        pass

    
post_save.connect(createProfile, sender=User)
post_save.connect(updateProfile, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)