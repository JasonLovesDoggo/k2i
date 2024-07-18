from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils import timezone

from .models import Opportunity, Resource, User, Scholarship


def home(request):
    """Homepage with featured opportunities, internships, and resources."""
    featured_internships = []
    featured_opportunities = Opportunity.objects.filter(apply_by__gt=timezone.now())[:3]
    featured_resources = Resource.objects.all()[:3]
    return render(
        request,
        "home.html",
        {
            "featured_internships": featured_internships,
            "featured_opportunities": featured_opportunities,
            "featured_resources": featured_resources,
        },
    )


def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_skills = user.skills.split(",") if user.skills else ["... Not specified ..."]
    user_interests = (
        user.interests.split(",") if user.interests else ["... Not specified ..."]
    )
    internships = user.applied_opportunities.filter(type="Internship")
    opportunities = user.applied_opportunities.exclude(type="Internship")
    
    return render(
        request,
        "profile.html",
        {
            "user": user,
            "user_skills": user_skills,
            "user_interests": user_interests,
            "internships": internships,
            "opportunities": opportunities,
        },
    )


def opportunity_list(request):
    """List of all available opportunities with filtering."""
    type_filter = request.GET.get("type")
    if type_filter:
        opportunities = Opportunity.objects.filter(is_closed=False, type=type_filter)
    else:
        opportunities = Opportunity.objects.filter(is_closed=False)

    type_choices = Opportunity.TYPE_CHOICES

    return render(
        request,
        "opportunity_list.html",
        {
            "opportunities": opportunities,
            "type_filter": type_filter,
            "type_choices": type_choices,
        },
    )


def opportunity_detail(request, pk):
    """Detail view for a single opportunity."""
    opportunity = get_object_or_404(Opportunity, pk=pk)
    return render(request, "opportunity_detail.html", {"opportunity": opportunity})


def resource_list(request):
    """List of all available resources."""
    resources = get_list_or_404(Resource)
    return render(request, "resource_list.html", {"resources": resources})


def scholarship_list(request):
    """List of all available scholarships."""
    scholarships = get_list_or_404(Scholarship)
    return render(request, "scholarship_list.html", {"scholarships": scholarships})


def scholarship_detail(request, pk):
    """Detail view for a single scholarship."""
    scholarship = get_object_or_404(Scholarship, pk=pk)
    return render(request, "scholarship_detail.html", {"scholarship": scholarship})

