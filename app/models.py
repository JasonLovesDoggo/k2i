import django.utils.timezone as timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    mentors = models.ManyToManyField("User", related_name="mentees", blank=True)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True)
    interests = models.CharField(max_length=255, blank=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        abstract = True


class Internship(Post):
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100, blank=True)
    stipend = models.IntegerField()
    apply_by = models.DateField()
    posted_on = models.DateTimeField(auto_now_add=True)
    applicants = models.ManyToManyField(User, related_name="applicants", blank=True)

    def __str__(self):
        return self.title


class Opportunity(Post):
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True)
    apply_by = models.DateField()
    stipend = models.IntegerField()
    applicants = models.ManyToManyField(User, related_name="applicants", blank=True)

    def __str__(self):
        return self.title

    def is_closed(self):
        return self.apply_by < timezone.now().date()


class Resource(Post):
    url = models.URLField()
    content = models.TextField(help_text="A brief description of the resource")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
