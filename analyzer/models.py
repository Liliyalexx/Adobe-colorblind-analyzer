from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class AnalysisResult(models.Model):
    COLORBLIND_TYPES = [
        ('protanopia', 'Protanopia (Red-Blind)'),
        ('deuteranopia', 'Deuteranopia (Green-Blind)'),
        ('tritanopia', 'Tritanopia (Blue-Blind)'),
        ('achromatomaly', 'Achromatomaly (Color Weakness)'),
    ]
    
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    colorblind_type = models.CharField(max_length=20, choices=COLORBLIND_TYPES)
    issues_count = models.PositiveIntegerField(default=0)
    screenshot = models.ImageField(upload_to='screenshots/', null=True, blank=True)
    analysis_data = models.JSONField(default=dict)

    def __str__(self):
        return f"Analysis of {self.url} for {self.get_colorblind_type_display()}"

    def clean(self):
        validator = URLValidator()
        try:
            validator(self.url)
        except ValidationError:
            raise ValidationError({'url': 'Enter a valid URL'})
        # models.py
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True) 
   
    def __str__(self):
        return f"Project {self.url} for {self.get_colorblind_type_display()}"