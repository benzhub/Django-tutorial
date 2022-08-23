from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):

    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page) # 顯示第幾頁
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page) # 沒有指定哪一頁的話，就顯示第1頁
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page) # 如果用戶訪問超過最大的頁面數的話，就顯示最後一頁

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles

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
