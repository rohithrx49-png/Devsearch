from dataclasses import field
from django.forms import ModelForm
from django import forms
from .models import marklist,Project

class markform(ModelForm):
    class Meta :
        model = marklist
        fields = '__all__'

class projectform(ModelForm):
    class Meta :
        model = Project
        fields = '__all__'
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }

    def __init__(self,*args,**kwargs):
        super(projectform,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        #self.fields['title'].widget.attrs.update({'class' : 'input','placeholder' : 'Add title'})