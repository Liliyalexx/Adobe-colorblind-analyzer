from django.urls import path
from .views import HomeView, AnalysisResultView, about, projects_index

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('result/<int:analysis_id>/', AnalysisResultView.as_view(), name='analysis_result'),
    path('about/', about, name='about'),
    path('projects/', projects_index, name='project-index' )
]
