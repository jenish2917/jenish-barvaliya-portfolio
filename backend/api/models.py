from django.db import models
from django.utils import timezone


class PersonalInfo(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    resume = models.URLField(blank=True)
    profile_image = models.URLField(blank=True, default="/images/profile.jpg")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"
    
    def __str__(self):
        return f"{self.name} - Personal Info"


class About(models.Model):
    summary = models.TextField()
    vision = models.TextField()
    highlights = models.JSONField(default=list)  # Store highlights as JSON array
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"
    
    def __str__(self):
        return "About Section"


class SocialLink(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    icon = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default="#ffffff")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} - {self.subject}"


class Project(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planned', 'Planned'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    long_description = models.TextField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    technologies = models.JSONField(default=list)  # Store as JSON array
    features = models.JSONField(default=list, blank=True)  # Store as JSON array
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming Languages'),
        ('ml_ai', 'Machine Learning & AI'),
        ('web_dev', 'Web Development'),
        ('data_science', 'Data Science & Analytics'),
        ('tools', 'Tools & Technologies'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    level = models.IntegerField(default=0, help_text="Skill level from 0-100")
    icon = models.CharField(max_length=50, default="💻")
    
    class Meta:
        ordering = ['category', '-level']
        
    def __str__(self):
        return f"{self.name} ({self.level}%)"


class Experience(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.JSONField(default=list)  # Store bullet points as JSON array
    technologies = models.JSONField(default=list)  # Store technologies as JSON array
    
    class Meta:
        ordering = ['-start_date']
        
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    @property
    def duration(self):
        if self.is_current:
            return f"{self.start_date.strftime('%B %Y')} - Present"
        elif self.end_date:
            return f"{self.start_date.strftime('%B %Y')} - {self.end_date.strftime('%B %Y')}"
        else:
            return f"{self.start_date.strftime('%B %Y')}"


class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=100)
    date_issued = models.DateField()
    credential_id = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    verification_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to='certifications/', blank=True, null=True)
    
    class Meta:
        ordering = ['-date_issued']
        
    def __str__(self):
        return f"{self.title} - {self.issuer}"


class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    gpa = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    coursework = models.JSONField(default=list)  # Store coursework as JSON array
    
    class Meta:
        ordering = ['-start_date']
        
    def __str__(self):
        return f"{self.degree} - {self.institution}"
    
    @property
    def duration(self):
        if self.is_current:
            return f"{self.start_date.year} - Present"
        elif self.end_date:
            return f"{self.start_date.year} - {self.end_date.year}"
        else:
            return f"{self.start_date.year}"
