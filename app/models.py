import django.utils.timezone as timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    mentors = models.ManyToManyField("User", related_name="mentees", blank=True)
    bio = models.TextField(blank=True)
    skills = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated list of skills"
    )
    interests = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated list of interests"
    )


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


class Opportunity(models.Model):
    INTERNSHIP = "Internship"
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"

    TYPE_CHOICES = [
        (INTERNSHIP, "Internship"),
        (FULL_TIME, "Full-time"),
        (PART_TIME, "Part-time"),
        (CONTRACT, "Contract"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    apply_by = models.DateField()
    location = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=INTERNSHIP)
    posted_on = models.DateField(auto_now_add=True)
    contact = models.EmailField(blank=True)
    stipend = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Resource(Post):
    url = models.URLField()
    content = models.TextField(help_text="A brief description of the resource")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
