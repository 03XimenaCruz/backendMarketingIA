from fastapi import APIRouter, HTTPException
from app.services.data_processing import DataProcessor
from app.services.visualization_service import VisualizationService

router = APIRouter()

@router.get("/sales-trend")
async def get_sales_trend():
    try:
        processor = DataProcessor()
        df = processor.process_data()
        processor.cluster_data()
        viz = VisualizationService(df, processor.scaled_df, processor.cluster_labels)
        return viz.get_sales_trend()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando tendencia de ventas: {str(e)}")

@router.get("/country-bar")
async def get_country_bar():
    try:
        processor = DataProcessor()
        df = processor.process_data()
        processor.cluster_data()
        viz = VisualizationService(df, processor.scaled_df, processor.cluster_labels)
        return viz.get_country_bar()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando gráfico de barras: {str(e)}")

@router.get("/histograms/{column}")
async def get_histograms(column: str):
    try:
        processor = DataProcessor()
        df = processor.process_data()
        processor.cluster_data()
        viz = VisualizationService(df, processor.scaled_df, processor.cluster_labels)
        return viz.get_histograms(column)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando histogramas: {str(e)}")

@router.get("/correlation-heatmap")
async def get_correlation_heatmap():
    try:
        processor = DataProcessor()
        df = processor.process_data()
        processor.cluster_data()
        viz = VisualizationService(df, processor.scaled_df, processor.cluster_labels)
        return viz.get_correlation_heatmap()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando mapa de calor: {str(e)}")

@router.get("/pca-scatter")
async def get_pca_scatter():
    try:
        processor = DataProcessor()
        df = processor.process_data()
        processor.cluster_data()
        viz = VisualizationService(df, processor.scaled_df, processor.cluster_labels)
        return viz.get_pca_scatter()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando dispersión PCA: {str(e)}")