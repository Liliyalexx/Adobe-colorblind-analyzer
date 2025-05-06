from django.urls import path
from .views import HomeView, CreateProjectView, AnalysisResultView, signup, login_view, about, project_list
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('about/', about, name='about'),
    path('projects/', project_list, name='project_list'),
    path('create/', CreateProjectView.as_view(), name='create_project'),
    path('analysis/<int:analysis_id>/', AnalysisResultView.as_view(), name='analysis_result'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('analysis/<int:analysis_id>/add_note/', views.add_note, name='add_note'),
    path('analysis/notes/<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('analysis/notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
]
