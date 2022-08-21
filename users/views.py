from pydoc import describe
from django.shortcuts import render
from .models import Profile

def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills   = profile.skill_set.exclude(description__exact="") # 排除描述為空值的description
    otherSkills = profile.skill_set.filter(description="") # 將描述為空值的description放進other Skill

    context= {
        "profile": profile,
        "topSkills": topSkills,
        "otherSkills": otherSkills
    }
    return render(request, 'users/user-profile.html', context)