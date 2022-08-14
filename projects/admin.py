from django.contrib import admin

# Register your models here.
from .models import Projects, Review, Tag

admin.site.register(Projects)
admin.site.register(Review)
admin.site.register(Tag)