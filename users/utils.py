from .models import Profile, Skill
from django.db.models import Q

def searchProfiles(request):
    search_query = ''

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")
        print(f"SEARCH: {search_query}")

    # skills = Skill.objects.filter(name__iexact=search_query) # 精確匹配
    skills = Skill.objects.filter(name__icontains=search_query) # 

    profiles = Profile.objects.distinct().filter( # distinct filter結果不重複
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)) # icontains大小寫不敏感查詢
    return profiles, search_query
