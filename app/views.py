from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.utils import timezone

from .models import Internship, Opportunity, Resource, User


def home(request):
    """Homepage with featured opportunities, internships, and resources."""
    featured_internships = Internship.objects.filter(
        posted_on__gte=timezone.now() - timezone.timedelta(days=30)
    )[:3]  # Recently posted
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


@login_required
def apply_to_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)

    if internship.apply_by < timezone.now().date():
        return render(
            request,
            "internship_detail.html",
            {"internship": internship, "application_closed": True},
        )  # Indicate that applications are closed

    if request.method == "POST":
        internship.applicants.add(
            request.user
        )  # Add the user to the internship's applicants
        return redirect(
            "internship_detail", pk=pk
        )  # Redirect back to the internship detail page  # In a real application, you'd likely send a confirmation email or redirect to a success page
    else:
        return render(
            request, "apply_to_internship.html", {"internship": internship}
        )  # Display an application form if it's a GET request


def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_skills = user.skills.split(",") if user.skills else []
    internships = user.internship_applications.all()
    opportunities = user.opportunities.all()

    return render(
        request,
        "profile.html",
        {
            "user": user,
            "user_skills": user_skills,
            "internships": internships,
            "opportunities": opportunities,
        },
    )


def internship_list(request):
    """List of all available internships."""
    current_internships = Internship.objects.filter(apply_by__gt=timezone.now())
    past_internships = Internship.objects.filter(apply_by__lte=timezone.now())

    return render(
        request,
        "internship_list.html",
        {
            "current_internships": current_internships,
            "past_internships": past_internships,
        },
    )


def internship_detail(request, pk):
    """Detail view for a single internship."""
    internship = get_object_or_404(Internship, pk=pk)
    return render(request, "internship_detail.html", {"internship": internship})


def opportunity_list(request):
    """List of all available opportunities."""
    opportunities = get_list_or_404(Opportunity, is_closed=False)
    return render(request, "opportunity_list.html", {"opportunities": opportunities})


def resource_list(request):
    """List of all available resources."""
    resources = get_list_or_404(Resource)
    return render(request, "resource_list.html", {"resources": resources})
