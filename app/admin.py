from django.contrib import admin

from .models import User, Opportunity, Resource
from unfold.admin import ModelAdmin


# Register your models here.
# from unfold.admin import ModelAdmin


class UserAdmin(ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")


class OpportunityAdmin(ModelAdmin):
    list_display = (
        "title",
        "type",
        "company",
        "location",
        "posted_on",
        "apply_by",
        "stipend",
    )
    search_fields = ("title", "company", "location", "type")


class ResourceAdmin(ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at")
    search_fields = ("title", "author")


admin.site.register(User, UserAdmin)
admin.site.register(Opportunity, OpportunityAdmin)
admin.site.register(Resource, ResourceAdmin)
