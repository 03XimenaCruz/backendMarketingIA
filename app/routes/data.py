from fastapi import APIRouter
from app.services.data_processing import DataProcessor

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