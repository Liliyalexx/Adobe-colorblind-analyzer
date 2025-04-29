import json
from django.shortcuts import render, redirect
from django.views import View
from .forms import UrlAnalysisForm
from .models import AnalysisResult
from .utils import analyze_website_for_colorblindness
from django.contrib import messages
from django.core.files.base import ContentFile
import base64
from selenium import webdriver



def about(request):
    return render(request, 'about.html')

class Project: 
    def __init__(self, name, description, date, status):
        self.name = name
        self.description = description
        self.date = date
        self.status = status

projects = [
    Project("AdobeMain", "main page of the adobe", "2025-04-28", 'completed'), 
    Project("NewsRu", "the website of newsru", "2025-04-28", 'in progress')
]

def projects_index(request):
    return render(request, 'projects/index.html', {'projects': projects})

class HomeView(View):
    template_name = 'analyzer/home.html'
        
    def get(self, request):
        form = UrlAnalysisForm()
        recent_analyses = AnalysisResult.objects.order_by('-created_at')[:5]
        return render(request, self.template_name, {
            'form': form,
            'recent_analyses': recent_analyses
        })
    
    def post(self, request):
        form = UrlAnalysisForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            colorblind_type = form.cleaned_data['colorblind_type']
            
            try:
                # Perform analysis
                analysis_data, screenshot_data = analyze_website_for_colorblindness(url, colorblind_type)
                
                # Create and save analysis result
                analysis = form.save(commit=False)
                analysis.issues_count = len(analysis_data.get('issues', []))
                analysis.analysis_data = analysis_data
                
                if screenshot_data:
                    # Convert base64 screenshot to image file
                    format, imgstr = screenshot_data.split(';base64,') 
                    ext = format.split('/')[-1]
                    screenshot_file = ContentFile(
                        base64.b64decode(imgstr), 
                        name=f"{url.replace('://', '_').replace('/', '_')}.{ext}"
                    )
                    analysis.screenshot = screenshot_file
                
                analysis.save()
                
                return redirect('analysis_result', analysis_id=analysis.id)
            
            except Exception as e:
                messages.error(request, f"Error analyzing website: {str(e)}")
        
        return render(request, self.template_name, {'form': form})

class AnalysisResultView(View):
    template_name = 'analyzer/result.html'
    
    def get(self, request, analysis_id):
        analysis = AnalysisResult.objects.get(id=analysis_id)
        return render(request, self.template_name, {
            'analysis': analysis,
            'issues': analysis.analysis_data.get('issues', []),
            'colorblind_type_display': analysis.get_colorblind_type_display()
        })