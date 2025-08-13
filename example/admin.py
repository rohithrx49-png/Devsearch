from django.contrib import admin
from .models import marklist,Project,Review,Tag
# Register your models here.

admin.site.register(marklist)
admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)
