from django.urls import pathfrom app import viewsurlpatterns = [	path("", views.home, name="index"),	path("profile", views.profile, name="profile"),	path("profile/<str:username>/", views.user_profile, name="profile"),	path("oppertunities", views.internship_list, name="opportunity_list"),	path("internships", views.internship_list, name="internship_list"),	path("resources", views.resource_list, name="resource_list"),	]