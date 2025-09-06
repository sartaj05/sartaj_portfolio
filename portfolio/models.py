from django.db import models
from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=300)
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title

class Experience(models.Model):
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    technologies = models.CharField(max_length=300)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-order']

    def __str__(self):
        return f"{self.position} at {self.company}"

class Skill(models.Model):
    SKILL_CATEGORIES = [
        ('programming', 'Programming Languages'),
        ('web', 'Web Technologies'),
        ('database', 'Databases'),
        ('framework', 'Frameworks'),
        ('tools', 'Tools & Libraries'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    proficiency = models.IntegerField(default=50, help_text="Proficiency level (0-100)")

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"Message from {self.name}"
    
    
    
# In portfolio/models.py, add:
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300)
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title