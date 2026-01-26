from rest_framework import serializers
from .models import DataSource

class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ['id', 'name', 'file', 'file_type', 'delimiter', 'created_at']