from django import forms
from .models import AnalysisResult, Project, Note


class UrlAnalysisForm(forms.ModelForm):
    class Meta:
        model = AnalysisResult
        fields = ['url', 'colorblind_type']
        widgets = {
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter website URL (e.g., https://example.com)'
            }),
            'colorblind_type': forms.Select(attrs={'class': 'form-select'})
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'website_url', 'description', 'image', 'is_completed']
        

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']
