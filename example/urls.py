from unicodedata import name
from django.urls import path
from .import views
urlpatterns = [
    path('',views.projects, name="projects"),
    path('project/<str:pk>/',views.project, name="project"),
    path('create-project/',views.createproject,name='createproject'),
    path('update-project/<str:pk>',views.updateproject,name='updateproject'),
    path('delete-project/<str:pk>',views.deleteproject,name='deleteproject'),
    
    
]