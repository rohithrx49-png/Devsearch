from multiprocessing import context
from django.shortcuts import render,HttpResponse,redirect
from .models import Profile
from example.models import Project
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm,ProfileForm,SkillForm
from .utils import searchProfiles,paginateProfiles

# Create your views here.

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request,'Username or password is incorrect')

    return render(request,'login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request,'User was logged out')
    return redirect('login')



def profiles(request):
    profiles,text = searchProfiles(request)
    #profiles = Profile.objects.all()
    custom_range,profiles = paginateProfiles(request,profiles,3)
    context = {'profiles':profiles,'text':text,'custom_range':custom_range}
    return render(request,"profiles.html",context)


def userprofile(request,pk):
    profile = Profile.objects.get(id=pk)
    topskills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")
    context = {'profile':profile,'topskills':topskills,'otherskills':otherskills}
    return render(request,"user-profile.html",context)


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request,'User account was created!')

            login(request,user)
            return redirect('edit-account')

        else:
            messages.success(request,'An error has occured during registration')
    context = {'page':page,'form':form}
    return render(request,'login_register.html',context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = Project.objects.all()
    context ={'profile':profile,'skills':skills,'projects':projects}
    return render(request,'account.html',context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form':form}
    return render(request,'profile_form.html',context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'Skill was added successfully!')
            return redirect('account')

    context = {'form':form}
    return render(request,'skill_form.html',context)


@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,'Skill was updated successfully!')
            return redirect('account')

    context = {'form':form}
    return render(request,'skill_form.html',context)


def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request,'Skill was deleted successfully!')
        return redirect('account')
    context = {'object':skill}
    return render(request,'delete_template.html',context)