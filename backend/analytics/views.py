from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from data_manager.models import DataSource
from .models import AnalysisResult
from .utils import load_dataset
import pandas as pd

# --- 1. The Summary View (For the "Preview" Button) ---
class AnalysisSummaryView(APIView):
    def get(self, request, pk):
        # Retrieve the pre-calculated summary from DB
        data_source = get_object_or_404(DataSource, pk=pk, owner=request.user)
        
        try:
            result = data_source.analysis # Access the OneToOne relation
            return Response({
                "filename": data_source.name,
                "total_rows": result.total_rows,
                "columns": result.column_types,
                "summary": result.basic_stats
            })
        except AnalysisResult.DoesNotExist:
            return Response({"status": "processing", "message": "Summary is being generated..."}, status=202)