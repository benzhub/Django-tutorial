from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles

def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
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
            return redirect(request.GET['next'] if 'next' in request.GET else 'account') # 如果有存在前一頁，登入後就立即返回前一頁，如果沒有就跳轉到account頁面
        else:
            messages.error(request, "Username OR Password is incorrect!")
            # print("Username OR Password is incorrect!")
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, "User was logged out!")
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # 用戶創建前資訊預處理
            user.username = user.username.lower() # 將用戶username全部變成英文小寫
            user.save() # 真正保存用戶資料

            messages.success(request, "User account was created!")
            # 創建帳號完直接登入
            login(request, user)
            return redirect("edit-account")
        else:
            messages.error(request, "An error has occurred during registration!")
    context = {"page": page, "form": form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3) # 每3個一頁
    context = {"profiles": profiles, "search_query": search_query, "custom_range": custom_range}
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


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.projects_set.all()
    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("account")

    context = {
        "form": form
    }
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect("account")

    context = {"object": skill}
    return render(request, 'delete_template.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {"messageRequests": messageRequests, "unreadCount": unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, 'users/message.html', context)

def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "You message was successfully sent!")
            return redirect("user-profile", pk=recipient.id)

    context = {"recipient": recipient, "form": form}
    return render(request, 'users/message_form.html', context)