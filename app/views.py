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


@login_required
def profile(request):
	user = get_object_or_404(User, username=request.user.username)
	internships = Internship.objects.filter(author=user)
	opportunities = Opportunity.objects.filter(author=user)
	resources = Resource.objects.filter(author=user)
	return render(
		request,
		"profile.html",
		{
			"user_skills": user.skills.split(",") if user.skills else ["No skills listed"],
			"user": user,
			"internships": internships,
			"opportunities": opportunities,
			"resources": resources,
		},
	)


@login_required
def user_profile(request, username):
	user = get_object_or_404(User, username=username)
	return render(request, "user_profile.html", {"user": user, "user_skills": user.skills.split(",") if user.skills else ["No skills listed"]})


def internship_list(request):
	"""List of all available internships."""
	internships = get_list_or_404(Internship)
	return render(request, 'internship_list.html', {'internships': internships})


def opportunity_list(request):
	"""List of all available opportunities."""
	opportunities = get_list_or_404(Opportunity, is_closed=False)
	return render(request, 'opportunity_list.html', {'opportunities': opportunities})


def resource_list(request):
	"""List of all available resources."""
	resources = get_list_or_404(Resource)
	return render(request, 'resource_list.html', {'resources': resources})
