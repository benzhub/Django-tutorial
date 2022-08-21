from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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

def deleteUser(sender, instance, **kwargs):
    user = instance.user # Profile被刪除時，User也被刪除
    user.delete()
    print("Deleting user...")
    
post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Profile)