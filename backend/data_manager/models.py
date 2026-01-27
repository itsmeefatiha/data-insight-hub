import os
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class DataSource(models.Model):
    DATA_TYPES = (
        ('csv', 'CSV File'),
        ('excel', 'Excel File'),
        ('xml', 'XML File'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='data_sources')
    name = models.CharField(max_length=200)
    
    file = models.FileField(
        upload_to='uploads/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['csv', 'xlsx', 'xls', 'xml'])]
    )
    
    file_type = models.CharField(max_length=10, choices=DATA_TYPES, default='csv')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 3. Enhanced Auto-detection
        ext = os.path.splitext(self.file.name)[1].lower()
        
        if ext == '.csv':
            self.file_type = 'csv'
        elif ext in ['.xlsx', '.xls']:
            self.file_type = 'excel'
        elif ext == '.xml':
            self.file_type = 'xml'
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.file_type})"