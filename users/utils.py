from .models import Skill,Profile
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def searchprofiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.filter(Q(name__icontains=search_query)|Q(short_intro__icontains=search_query)|Q(skill__in=skills)).distinct()
    return profiles


def paginateprofiles(request,profiles,num):
    paginator = Paginator(profiles,num)

    page = request.GET.get('page')

    try:
        page_profiles = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        page_profiles = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        page_profiles = paginator.page(page)

    leftindex = int(page)-2
    if leftindex <1:
        leftindex = 1
    rightindex = int(page)+2
    if rightindex >paginator.num_pages:
        rightindex = paginator.num_pages+1

    custom_range = range(leftindex,rightindex)



    return page_profiles,custom_range

