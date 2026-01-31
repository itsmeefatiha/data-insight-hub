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

# --- 2. The Table View (For the "Full Data" Scroll) ---
class DataFramePagination(PageNumberPagination):
    page_size = 50 # Send 50 rows at a time (Crucial for performance)
    page_size_query_param = 'page_size'

class FileTableView(APIView):
    def get(self, request, pk):
        data_source = get_object_or_404(DataSource, pk=pk, owner=request.user)
        
        try:
            df = load_dataset(data_source.file.path)
            
            # Convert DataFrame to a list of dicts: [{"col1": 1}, {"col1": 2}...]
            # Replace NaNs with None for valid JSON
            data = df.where(pd.notnull(df), None).to_dict(orient='records')
            
            # Use Pagination (So 100k rows don't freeze the browser)
            paginator = DataFramePagination()
            result_page = paginator.paginate_queryset(data, request)
            
            return paginator.get_paginated_response(result_page)
            
        except Exception as e:
            return Response({"error": str(e)}, status=400)