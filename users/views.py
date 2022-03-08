from email import message
from django.shortcuts import render,redirect
from .models import Message, Profile,Skill
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import Customusercreationform, Profileform,Skillform,Messageform
from django.contrib.auth.decorators import login_required
from .utils import searchprofiles,paginateprofiles
from django.db.models import Q

# Create your views here.

def profiles(request):
    profiles = searchprofiles(request)
    page_profiles,custom_range = paginateprofiles(request,profiles,3)
    context = {
        'profiles':page_profiles,
        'custom_range':custom_range,
    }

    return render(request,'users/all-profiles.html',context)


def profile(request,pk):
    profile = Profile.objects.get(id=pk)

    topskill = profile.skill_set.exclude(description='')

    otherskill = profile.skill_set.filter(description='')


    context={
        'profile':profile,'topskill':topskill,'otherskill':otherskill,
    }

    return render(request,'users/single-profile.html',context)


def loginuser(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('projects:projects')

    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)

        except Exception as e:
            print(e)
            messages.error(request,'user does not exist')

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'user logged in')
            return redirect(request.GET['next']if 'next' in request.GET else 'users:account')
        else:
            messages.error(request,"username and password doesnot match")

    context={'page':page}
    
    return render(request,'users/login_register.html',context)


def logoutuser(request):
    logout(request)
    messages.success(request,"user logged out")
    return redirect('users:login')

def registeruser(request):
    page = 'register'

    form = Customusercreationform()

    if request.method =='POST':
        form = Customusercreationform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,'user created successfully')
            return redirect ('users:login')
        else:
            messages.error(request,'some error occured')

    context={'page':page,'form':form}
    return render(request,'users/login_register.html',context)


@login_required(login_url='users:login')
def useraccount(request):
    profile = request.user.profile

    context={'profile':profile}
    return render(request,'users/account.html',context)


@login_required(login_url='users:login')
def editprofile(request):
    profile = request.user.profile
    form = Profileform(instance=profile)

    if request.method =='POST':
        form = Profileform(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'profile updated successfully')
            return redirect('users:account')

    context={'form':form}

    return render(request,'users/editprofile.html',context)


@login_required(login_url='users:login')
def createskill(request):
    profile = request.user.profile
    form = Skillform()

    if request.method =='POST':
        form = Skillform(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'skill created successfully')
            return redirect ('users:account')
        else:
            messages.error(request,'some error occured')

    context={'form':form}

    return render(request,'users/skillform.html',context)



@login_required(login_url='users:login')
def updateskill(request,pk):
    profile = request.user.profile
    skillobj = profile.skill_set.get(id=pk)

    form = Skillform(instance=skillobj)

    if request.method =='POST':
        form = Skillform(request.POST,instance=skillobj)
        if form.is_valid():
            form.save()
            messages.success(request,'skill updated successfully')
            return redirect ('users:account')
        else:
            messages.error(request,'some error occured')

    context={'form':form}

    return render(request,'users/skillform.html',context)



@login_required(login_url='users:login')
def deleteskill(request,pk):
    profile = request.user.profile
    skillobj = profile.skill_set.get(id=pk)

    form = Skillform(request.POST,instance=skillobj)

    if request.method =='POST':
        skillobj.delete()
        messages.success(request,'skill deleted successfully')
        return redirect ('users:account')

    context={'object':skillobj}

    return render(request,'delete-template.html',context)


@login_required(login_url='users:login')
def inbox(request):
    recipient = request.user.profile
    received_msg = recipient.messages.all()
    unreadcount = received_msg.filter(is_read=False).count()

    
    context={'received_msg':received_msg,'unreadcount':unreadcount}

    return render(request,'users/inbox.html',context)


@login_required(login_url='users:login')
def viewmessage(request,pk):
    message = Message.objects.get(id=pk)
    if message.is_read == False:
        message.is_read =True
        message.save()

    context={'message':message}

    return render(request,'users/message.html',context)

def createmessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = Messageform()

    if request.method =='POST':
        form = Messageform(request.POST)
        try:
            sender = request.user.profile
        except:
            sender =None
        if form.is_valid():
            message = form.save(commit=False)
            message.seder = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request,'message sent successfully')
            return redirect('users:all-profile')

    context = {'form':form,'recipient':recipient}
    return render(request,'users/message-form.html',context)
            

        





