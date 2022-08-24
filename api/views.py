from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
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
# @permission_classes([IsAuthenticated]) # 需要登入拿到token才有權限可以使用
def getProjects(request):
    print(f"user: {request.user}")
    print(f"user: {request.user.id}")
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True) # 返回多個就要設定many=True
    return Response(serializer.data)

@api_view(["GET"])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False) # 返回1個就要設定many=False
    return Response(serializer.data)