from fastapi import APIRouter
from app.services.data_processing import DataProcessor
import os

router = APIRouter()

@router.get("/dataframe")
async def get_dataframe():
    processor = DataProcessor()
    df = processor.process_data()
    return df.to_dict(orient='records')

@router.get("/clusters")
async def get_clusters():
    processor = DataProcessor()
    processor.process_data()
    labels = processor.cluster_data()
    return {"labels": labels.tolist()}

@router.get("/pca")
async def get_pca():
    processor = DataProcessor()
    processor.process_data()
    processor.cluster_data()
    pca_data = processor.apply_pca()
    return pca_data

@router.get("/debug/files")
async def debug_files():
    try:
        data_path = os.getenv("DATA_PATH", "data/sales_data_sample.csv")
        files = os.listdir(os.path.dirname(data_path))
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}