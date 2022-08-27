from tkinter import Widget
from django.forms import ModelForm
from django import forms
from .models import Projects as Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link']

        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **keargs):
        super(ProjectForm, self).__init__(*args, **keargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})

        # self.fields["title"].widget.attrs.update({"class": "input"})
        # self.fields["description"].widget.attrs.update({"class": "input"})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["value", "body"]
        labels = {
            "value": "Place your vote",
            "body": "Add your comment with your vote!"
        }
    def __init__(self, *args, **keargs):
        super(ReviewForm, self).__init__(*args, **keargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})