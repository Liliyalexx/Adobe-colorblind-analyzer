from django import forms
from .models import AnalysisResult

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