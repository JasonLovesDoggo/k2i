from django.contrib import admin

from .models import User, Internship, Opportunity, Resource

# Register your models here.
# from unfold.admin import ModelAdmin

admin.site.register(User)
admin.site.register(Internship)
admin.site.register(Opportunity)
admin.site.register(Resource)
