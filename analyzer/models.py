from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone


COLORBLIND_TYPES = [
    ('protanopia', 'Protanopia (Red-Blind)'),
    ('deuteranopia', 'Deuteranopia (Green-Blind)'),
    ('tritanopia', 'Tritanopia (Blue-Blind)'),
    ('achromatomaly', 'Achromatomaly (Color Weakness)'),
]

class AnalysisResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    colorblind_type = models.CharField(max_length=20, choices=COLORBLIND_TYPES)
    issues_count = models.PositiveIntegerField(default=0)
    screenshot = models.ImageField(upload_to='screenshots/', null=True, blank=True)
    analysis_data = models.JSONField(default=dict)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='analyses',null=True, blank=True)
    project_name = models.CharField(max_length=100, blank=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
            # Extract domain as project name
        from urllib.parse import urlparse
        domain = urlparse(self.url).netloc
        self.project_name = domain.replace('www.', '').split('.')[0] + '.' + domain.split('.')[-1]
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Analysis of {self.url} for {self.get_colorblind_type_display()}"

    def clean(self):
        validator = URLValidator()
        try:
            validator(self.url)
        except ValidationError:
            raise ValidationError({'url': 'Enter a valid URL'})
       
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    website_url = models.URLField(max_length=500, blank=True) 
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Project: {self.name}"
    
    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return f"Project: {self.name}"
    
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    analysis = models.ForeignKey(AnalysisResult, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.analysis.url}"
