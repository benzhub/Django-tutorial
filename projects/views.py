from cgi import print_directory
from turtle import right
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Projects as Project
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects

def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6) # 每６個一頁

    context = {
        'projects': projects,
        'search_query': search_query, 
        'custom_range': custom_range
        }
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        try:
            
            form = ReviewForm(request.POST)
            review = form.save(commit=False)
            review.projects = projectObj
            review.owner = request.user.profile
            
            review.save()

            projectObj.getVoteCount

            messages.success(request, 'Your review was successfully submitted!')
            return redirect('project', pk=projectObj.id)
        except:
            messages.error(request, 'Your review had some error!')
            return redirect('project', pk=projectObj.id)


    return render(request, 'projects/single-project.html', {'project': projectObj, 'form': form})

@login_required(login_url="login") # 如果沒有登入，就重定向到登入頁面
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        # print(request.POST)
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {
        'form': form
    }
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login") # 如果沒有登入，就重定向到登入頁面
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.projects_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        # print(request.POST)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {
        'form': form
    }
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login") # 如果沒有登入，就重定向到登入頁面
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.projects_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {
        'object': project
    }
    return render(request, 'delete_template.html', context)