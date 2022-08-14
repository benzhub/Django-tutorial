from django.shortcuts import render
from django.http import HttpResponse

projectList = [
    {
        "id": "1",
        "title": "Ecommerce Website",
        "description": "Fully functional ecommerce website"
    },
    {
        "id": "2",
        "title": "Portfolio Webstie",
        "description": "This was a project where I built out my portfol"
    },
    {
        "id": "3",
        "title": "Social Network",
        "description": "Awesome open source project I am still working"
    },
]

def projects(request):
    page = "Projects"
    number = 10
    context = {
        'page': page,
        'number': number,
        'projects': projectList
    }
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = None
    for i in projectList:
        if i['id'] == str(pk):
            projectObj = i
    context = {
        'project': projectObj
    }
    return render(request, 'projects/single-project.html', context)