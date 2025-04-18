from django.contrib import admin
from .models import User, Course, Section, Lab, Assignment


# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Lab)
admin.site.register(Assignment)
