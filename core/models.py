from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MinLengthValidator
from django.conf import settings

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=250, help_text="Brief description for projects listing page")
    description = models.JSONField(
        help_text="""
        Format: [
            {"type": "heading", "content": "Overview"},
            {"type": "text", "content": "Project description here"},
            {"type": "heading", "content": "Challenges"},
            {"type": "text", "content": "Challenges faced..."}
        ]
        """
    )
    category = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    technologies = models.JSONField(
        help_text="""
        Format: [
            {"name": "React"},
            {"name": "Django"}
        ]
        """
    )
    featured_image = models.ImageField(upload_to='projects/')
    live_url = models.URLField(blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    timeline = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    date_created = models.DateField()
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if not isinstance(self.description, list):
            raise ValidationError({'description': 'Content must be a list of sections'})
        
        for item in self.description:
            if not isinstance(item, dict):
                raise ValidationError({'description': 'Each section must be a dictionary'})
            if 'type' not in item or 'content' not in item:
                raise ValidationError({'description': 'Each section must have type and content'})
            if item['type'] not in ['heading', 'text']:
                raise ValidationError({'description': 'Section type must be either heading or text'})

        if not isinstance(self.technologies, list):
            raise ValidationError({'technologies': 'Technologies must be a list'})
        
        for tech in self.technologies:
            if not isinstance(tech, dict) or 'name' not in tech:
                raise ValidationError({'technologies': 'Each technology must be a dictionary with at least a name'})

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Gallery image {self.order} for {self.project.title}"

class Skill(models.Model):
    name = models.CharField(max_length=100)  # e.g., "React", "Vue.js"
    icon_url = models.URLField(
        help_text="URL from devicons (e.g., https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg)"
    )
    description = models.CharField(max_length=100)  # e.g., "Frontend Development", "Progressive Framework"
    order = models.PositiveIntegerField(default=0, help_text="Display order in the skills grid")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    ip_address = models.GenericIPAddressField()
    date_sent = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_sent']
        verbose_name_plural = 'Contact Messages'
    
    def clean(self):
        super().clean()
        
        recent_messages = Contact.objects.filter(
            ip_address=self.ip_address,
            date_sent__gte=timezone.now() - timezone.timedelta(hours=24)
        ).count()
        
        if recent_messages >= getattr(settings, 'MAX_CONTACT_MESSAGES_PER_DAY', 5):
            raise ValidationError('Too many messages. Please try again later.')
    
    def __str__(self):
        return f"Message from {self.name} ({self.date_sent.strftime('%Y-%m-%d')})"
