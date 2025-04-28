from django.urls import path
from .views import HomeView, AnalysisResultView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('result/<int:analysis_id>/', AnalysisResultView.as_view(), name='analysis_result'),
]