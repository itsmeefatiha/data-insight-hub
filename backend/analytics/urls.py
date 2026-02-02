from django.urls import path
from .views import AnalysisSummaryView, FileTableView, CustomMetricView

urlpatterns = [
    # 1. Get the Summary (Profile)
    path('summary/<int:pk>/', AnalysisSummaryView.as_view(), name='file-summary'),
    
    # 2. Get the Full Data (Paginated)
    # Usage: /api/analytics/data/1/?page=1
    path('data/<int:pk>/', FileTableView.as_view(), name='file-data'),
    
    # 3. Calculate something specific
    path('calculate/<int:pk>/', CustomMetricView.as_view(), name='custom-metric'),
]