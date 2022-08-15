from django.forms import ModelForm
from .models import Projects as Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'