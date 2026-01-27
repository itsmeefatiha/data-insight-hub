from django.db import models
from data_manager.models import DataSource

class AnalysisResult(models.Model):

    data_source = models.OneToOneField(DataSource, on_delete=models.CASCADE, related_name='analysis')
    total_rows = models.IntegerField(default=0)
    total_columns = models.IntegerField(default=0)
    column_types = models.JSONField(default=dict) # {"age": "numeric", "city": "text"}
    basic_stats = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.data_source.name}"