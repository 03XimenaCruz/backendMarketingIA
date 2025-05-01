# backend/test_csv.py
import pandas as pd

df = pd.read_csv('data/sales_data_sample.csv', encoding='latin1')
print("Columnas:", df.columns.tolist())
print("Valores NaN por columna:", df.isna().sum().to_dict())
print("Tipos de datos:", df.dtypes.to_dict())
print("Valores únicos de COUNTRY:", df['COUNTRY'].unique())
print("Tipo de datos de SALES:", df['SALES'].dtype)
print("Valores NaN en SALES:", df['SALES'].isna().sum())
print("Valores únicos de SALES (primeros 10):", df['SALES'].dropna().head(10).tolist())