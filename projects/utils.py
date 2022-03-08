from .models import Tag,Project
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def searchprojects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.filter(Q(title__icontains=search_query)|Q(owner__name__icontains=search_query)|Q(tags__in=tags)).distinct()
    return projects



def paginateprojects(request,projects,num):
    paginator = Paginator(projects,num)

    page = request.GET.get('page')

    try:
        page_projects = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        page_projects = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        page_projects = paginator.page(page)

    leftindex = int(page)-2
    if leftindex <1:
        leftindex = 1
    rightindex = int(page)+2
    if rightindex >paginator.num_pages:
        rightindex = paginator.num_pages+1

    custom_range = range(leftindex,rightindex)



    return page_projects,custom_range
