from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project,Tag
from .forms import projectform
from .utils import searchProjects,paginateProjects

# Create your views here.

#projectList = [{'id':'1','title':"Ecommerce Website",'description':'Fully functional website'},
#{'id':'2','title':"Portfolio Website",'description':'Fully functional website'},
#{'id':'3','title':"Social Network",'description':'Fully functional website'},]

def projects(request):
    projects,text = searchProjects(request)
    #projects = Project.objects.all()
    custom_range,projects = paginateProjects(request,projects,6)


    context = {'projects':projects,'text':text,'custom_range':custom_range}
    return render(request,'projects/projects.html',context)

def project(request,pk):
    projectobj = Project.objects.get(id=pk)
    return render(request,'projects/single-project.html',{'project':projectobj})

@login_required(login_url="login")
def createproject(request):
    profile = request.user.profile
    form = projectform()
    if request.method == 'POST':
        form = projectform(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {'form':form}
    return render(request,'projects/projectform.html',context)

@login_required(login_url="login")
def updateproject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = projectform(instance=project)
    if request.method == 'POST':
        form = projectform(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request,'projects/projectform.html',context) 

@login_required(login_url="login")    
def deleteproject(request,pk):
    profile = request.user.profile
    project1 = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project1.delete()
        return redirect('account')
    context = {'object':project1}
    return render(request,'delete_template.html',context)
    