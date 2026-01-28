import pandas as pd
import os
from .models import AnalysisResult

def load_dataset(file_path):
    """Helper to read files"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        return pd.read_csv(file_path, sep=None, engine='python') # Auto-detect delimiter
    elif ext in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    elif ext == '.xml':
        return pd.read_xml(file_path)
    raise ValueError("Unsupported format")

def generate_summary(data_source_instance):
    """
    1. Opens the file.
    2. Calculates df.describe().
    3. Saves AnalysisResult to DB.
    """
    try:
        df = load_dataset(data_source_instance.file.path)
        
        # Calculate Metadata
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()

        summary = df.describe(include='all').where(pd.notnull(df), None).to_dict()
        
        # Save to DB
        AnalysisResult.objects.create(
            data_source=data_source_instance,
            total_rows=len(df),
            total_columns=len(df.columns),
            # We save the column types so React knows what options to show
            column_types={"numeric": numeric_cols, "categorical": cat_cols},
            basic_stats=summary
        )
        print(f"✅ Summary generated for {data_source_instance.name}")
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")