from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class DataSource(models.Model):
    DATA_TYPES = (
        ('csv', 'CSV File'),
        ('excel', 'Excel File'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='data_sources')
    name = models.CharField(max_length=200)
    
    file = models.FileField(
        upload_to='uploads/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['csv', 'xlsx', 'xls'])]
    )
    
    file_type = models.CharField(max_length=10, choices=DATA_TYPES, default='csv')
    
    delimiter = models.CharField(max_length=1, default=',')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-detect type based on extension
        if self.file.name.endswith('.csv'):
            self.file_type = 'csv'
        else:
            self.file_type = 'excel'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.owner.email})"