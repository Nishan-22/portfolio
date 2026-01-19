from django.db import models

from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    bio = models.TextField()
    location = models.CharField(max_length=100, default="Remote")

    # ✅ ADD THESE
    email = models.EmailField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=50)
    icon_name = models.CharField(max_length=50, help_text="FontAwesome icon name, e.g., 'python'")

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True)
    link = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
