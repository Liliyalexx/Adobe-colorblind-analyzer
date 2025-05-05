import base64
import json
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from django.http import HttpResponseNotAllowed
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.files.base import ContentFile
from django.db.models import Max, OuterRef, Subquery
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import UrlAnalysisForm, ProjectForm, NoteForm
from .models import AnalysisResult, Project, Note
from .utils import analyze_website_for_colorblindness, run_colorblind_analysis
from django.db import models



def home(request):
    if request.method == 'POST':
        form = UrlAnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.save()
            return redirect('analysis_result', analysis.id)
    else:
        form = UrlAnalysisForm()

    recent_analyses = AnalysisResult.objects.order_by('-created_at')[:5]
    
    return render(request, 'analyzer/home.html', {
        'form': form,
        'recent_analyses': recent_analyses,
    })


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'analyzer/home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get analyses either through direct user relation or through project
        context['recent_analyses'] = AnalysisResult.objects.filter(
            models.Q(user=self.request.user) | 
            models.Q(project__user=self.request.user)
        ).distinct().order_by('-created_at')[:10]
        
        # Add form to context
        context['form'] = UrlAnalysisForm()
        return context
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('project_list') 
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')
def about(request):
    return render(request, 'about.html')

@login_required(login_url='login')
def project_list(request):
    # Get projects for the current user
    projects = Project.objects.filter(user=request.user).order_by('-created_at')
    form = NoteForm()
    # Get the latest analysis for each project
    latest_analysis = AnalysisResult.objects.filter(
        project=OuterRef('pk')
    ).order_by('-created_at')

    # Annotate each project with its latest analysis details
    projects = projects.annotate(
        latest_issues=Subquery(latest_analysis.values('issues_count')[:1]),
        latest_type=Subquery(latest_analysis.values('colorblind_type')[:1]),
        latest_created=Subquery(latest_analysis.values('created_at')[:1]),
    )
    for project in projects:
        project.notes = Note.objects.filter(analysis__project=project).order_by('-created_at')
    return render(request, 'projects/project_list.html', {
        'projects': projects,'form': form
        }
    )
def projects_view(request):
    # Get all distinct project names
    project_names = AnalysisResult.objects.values_list('project_name', flat=True).distinct()

    # For each project name, get the latest test
    projects = []
    for name in project_names:
        latest = (
            AnalysisResult.objects
            .filter(project_name=name)
            .order_by('-created_at')
            .first()
        )
        if latest:
            projects.append({
                'name': name,
                'latest_type': latest.get_colorblind_type_display(),
                'latest_issues': latest.issues_count,
                'latest_created': latest.created_at
            })

    return render(request, 'project_list.html', {'projects': projects})

def extract_first_image_url(website_url):
    try:
        response = requests.get(website_url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            src = img['src']
            # Handle relative URLs
            if src.startswith('http'):
                return src
            else:
                return requests.compat.urljoin(website_url, src)
    except Exception as e:
        print(f"Image fetch failed: {e}")
    return None

def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('project_list')
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')  # Redirect to project list after save
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})
projects = [
    Project("AdobeMain", "main page of the adobe", "2025-04-28", 'completed'), 
    Project("NewsRu", "the website of newsru", "2025-04-28", 'in progress')
]

def projects_index(request):
    return render(request, 'projects/index.html', {'projects': projects})

        
@login_required
def add_note(request, analysis_id):
    analysis = get_object_or_404(AnalysisResult, pk=analysis_id)

    if request.method == 'POST':
        note_text = request.POST.get('note')
        if note_text:
            Note.objects.create(analysis=analysis, text=note_text,  user=request.user )
        return redirect('analysis_result', analysis_id=analysis.id)
    else:
        return render(request, 'note_not_allowed.html', {'analysis': analysis})
        

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.user != request.user:
        return redirect('analysis_results', analysis_id=note.analysis.id) 
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('analysis_results', analysis_id=note.analysis.id)
    else:
        form = NoteForm(instance=note)
    return render(request, 'edit_note.html', {'form': form, 'note': note})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.user == request.user:
        note.delete()

class CreateProjectView(View):
    template_name = 'analyzer/create_project.html'

    def get(self, request):
        form = UrlAnalysisForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UrlAnalysisForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            colorblind_type = form.cleaned_data['colorblind_type']

            try:
                # Parse domain to use as project name
                domain = urlparse(url).netloc
                project_name = domain.replace('www.', '').split('.')[0]

                # Get or create Project for the user
                project, created = Project.objects.get_or_create(
                    name=project_name,
                    user=request.user,
                    defaults={
                        'website_url': url,
                        'description': f"Automatically created project for {url}",
                        'date': timezone.now().date()
                    }
                )

                # Run colorblind analysis
                analysis_data, screenshot_data = analyze_website_for_colorblindness(url, colorblind_type)

                # Create new AnalysisResult instance
                analysis = form.save(commit=False)
                analysis.user = request.user
                analysis.project = project
                analysis.issues_count = len(analysis_data.get('issues', []))
                analysis.analysis_data = analysis_data

                # Save screenshot if present
                if screenshot_data:
                    format, imgstr = screenshot_data.split(';base64,')
                    ext = format.split('/')[-1]
                    screenshot_file = ContentFile(base64.b64decode(imgstr), name=f"screenshot.{ext}")
                    analysis.screenshot = screenshot_file

                analysis.save()

                return redirect('analysis_result', analysis_id=analysis.id)

            except Exception as e:
                messages.error(request, f"Error during analysis: {str(e)}")

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

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
