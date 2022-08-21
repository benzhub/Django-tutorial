from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile

def loginUser(request):
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist.")
            # print("Username does not exist")
        # 確認帳號密碼
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # 在資料庫中創建session，在瀏覽器中放置cookie
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "Username OR Password is incorrect!")
            # print("Username OR Password is incorrect!")
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

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