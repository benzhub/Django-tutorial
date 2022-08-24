from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Projects as Project

@api_view(["GET"])
def getRoutes(request):
    routes = [
        {"GET": "/api/projects"},
        {"GET": "/api/projects/id"},
        {"POST": "/api/projects/id/vote"},

        {"GET": "/api/users/token"},
        {"GET": "/api/users/token/refresh"},
    ]
    # return JsonResponse(routes, safe=False) # 因為return 不是json格式，所以safe=False
    return Response(routes) 

@api_view(["GET"])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True) # 返回多個就要設定many=True
    return Response(serializer.data)

@api_view(["GET"])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False) # 返回1個就要設定many=False
    return Response(serializer.data)