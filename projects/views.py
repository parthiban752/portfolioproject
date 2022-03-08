from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import HttpResponse
#from portfolio.projects.utils import searchprojects
from projects.models import Project,Review,Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import searchprojects,paginateprojects
#from users.models import Profile

# Create your views here.


projectslist=[
    {
        'id':'1',
        'title':'ecommerce website',
        'description':'fully functional ecommerce wesite'
    },
    {
        'id':'2',
        'title':'portfolio website',
        'description':'peersonal website to write articles'
    },
    {
        'id':'3',
        'title':'social network',
        'description':'open source project for community'
    }
]





def projects(request):
    projects = searchprojects(request)
    #projects= Project.objects.all().order_by('-vote_ratio','-vote_total')
    page_projects,custom_range = paginateprojects(request,projects,3)
    context ={
        'projects':page_projects,
        'custom_range':custom_range
    }
    return render(request,'projects/projects.html',context)

def project(request,pk):
    proj_obj = Project.objects.get(id=pk)
    tags=proj_obj.tags.all()

    reviews = proj_obj.review_set.all()


    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid:
            review = form.save(commit=False)
            review.project = proj_obj
            review.owner = request.user.profile
            review.save()

            proj_obj.getvotecount

            messages.success(request,'comment submitted successfully')
            return redirect('projects:project',pk=proj_obj.id)

        else:
            messages.error(request,'some error occured')


    context={'proj':proj_obj,'tags':tags,'reviews':reviews,'form':form}

    return render(request,'projects/project.html',context)

@login_required(login_url='users:login')
def createProject(request):
    profile = request.user.profile
    form=ProjectForm()

    if request.method == 'POST':
        form= ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request,'project created successfully')
            return redirect('users:account')
    context={'form':form,}
    return render(request,'projects/project-form.html',context)


@login_required(login_url='users:login')
def updateProject(request,pk):
    profile = request.user.profile
    projectobj=profile.project_set.get(id=pk)

    form=ProjectForm(instance=projectobj)

    if request.method == 'POST':
        form= ProjectForm(request.POST,instance=projectobj)
        if form.is_valid():
            form.save()
            messages.success(request,'project updated successfully')
            return redirect('users:account')
    context={'form':form,}
    return render(request,'projects/project-form.html',context)


@login_required(login_url='users:login')
def deleteProject(request,pk):
    profile = request.user.profile

    projobj=profile.project_set.get(id=pk)

    if request.method == 'POST':
        projobj.delete()
        messages.success(request,'project deleted successfully')
        return redirect('users:account')
    context={'object':projobj}
    return render(request,'delete-template.html',context)





