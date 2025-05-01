import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from dotenv import load_dotenv
import os

load_dotenv()

class DataProcessor:
    def __init__(self):
        self.file_path = os.getenv("DATA_PATH", "data/sales_data_sample.csv")
        print(f"Intentando cargar archivo desde: {self.file_path}")
        self.df = None
        self.scaled_df = None
        self.cluster_labels = None

    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_path, encoding='latin1')
            print("Columnas del DataFrame:", self.df.columns.tolist())
            print("Valores NaN por columna:", self.df.isna().sum().to_dict())
            print("Valores únicos de COUNTRY:", self.df['COUNTRY'].unique())

            # Verifica columnas requeridas
            required_columns = ['SALES', 'QUANTITYORDERED', 'PRODUCTCODE', 'PRICEEACH',
                                'ORDERLINENUMBER', 'COUNTRY', 'PRODUCTLINE', 'DEALSIZE',
                                'ORDERDATE', 'STATUS', 'QTR_ID', 'YEAR_ID']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            if missing_columns:
                raise ValueError(f"Faltan columnas en el CSV: {missing_columns}")

            # Convierte ORDERDATE y deriva MONTH_ID
            self.df['ORDERDATE'] = pd.to_datetime(self.df['ORDERDATE'], errors='coerce')
            self.df['MONTH_ID'] = self.df['ORDERDATE'].dt.month
            self.df['MONTH_ID'] = self.df['MONTH_ID'].fillna(0).astype(int)
            print("Valores NaN en MONTH_ID:", self.df['MONTH_ID'].isna().sum())

            # Codifica PRODUCTCODE
            self.df['PRODUCTCODE'] = pd.Categorical(self.df['PRODUCTCODE']).codes

            # Convierte columnas numéricas a numérico y maneja NaN
            numeric_columns = ['SALES', 'QUANTITYORDERED', 'PRICEEACH', 'ORDERLINENUMBER', 'QTR_ID', 'YEAR_ID']
            # Si MSRP está presente, agrégalo
            if 'MSRP' in self.df.columns:
                numeric_columns.append('MSRP')
            for col in numeric_columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
                print(f"Valores NaN en {col} después de conversión:", self.df[col].isna().sum())

            # Elimina columnas no necesarias (excluye QTR_ID, YEAR_ID, MONTH_ID)
            columns_to_drop = ['STATUS', 'ORDERDATE', 'ADDRESSLINE2', 'STATE', 'POSTALCODE', 'TERRITORY']
            self.df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

            # Verifica NaN después de eliminar columnas
            print("Valores NaN después de eliminar columnas:", self.df.isna().sum().to_dict())

            return self.df
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            raise

    def create_dummies(self, column):
        try:
            if column in self.df.columns:
                print(f"Valores únicos de {column} antes de limpieza:", self.df[column].unique())
                # Limpia NaN en la columna
                self.df[column] = self.df[column].fillna('Unknown')
                print(f"Valores únicos de {column} después de limpieza:", self.df[column].unique())
                dummy = pd.get_dummies(self.df[column], prefix=column)
                print(f"Columnas dummy generadas para {column}:", dummy.columns.tolist())
                # Convierte dummy a int (0 o 1) para evitar NaN
                dummy = dummy.astype(int)
                self.df.drop(columns=column, inplace=True)
                self.df = pd.concat([self.df, dummy], axis=1)
            else:
                print(f"Advertencia: La columna {column} no existe en el DataFrame")
        except Exception as e:
            print(f"Error en create_dummies para {column}: {str(e)}")
            raise

    def process_data(self):
        try:
            self.load_data()
            self.create_dummies('COUNTRY')
            self.create_dummies('PRODUCTLINE')
            self.create_dummies('DEALSIZE')
            # Verifica NaN en el DataFrame final
            if self.df.isna().any().any():
                print("Advertencia: Valores NaN detectados en el DataFrame final")
                self.df = self.df.fillna(0)
            print("Columnas después de procesar:", self.df.columns.tolist())
            print("Valores NaN en el DataFrame final:", self.df.isna().sum().to_dict())
            return self.df
        except Exception as e:
            print(f"Error en process_data: {str(e)}")
            raise

    def cluster_data(self, n_clusters=5):
        try:
            print("Ejecutando cluster_data")
            numeric_features = self.df.select_dtypes(include=np.number).columns
            print("Características numéricas:", numeric_features.tolist())
            scaler = StandardScaler()
            self.scaled_df = scaler.fit_transform(self.df[numeric_features].fillna(0))
            print("Forma de scaled_df después de escalar:", self.scaled_df.shape)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            self.cluster_labels = kmeans.fit_predict(self.scaled_df)
            print("Longitud de cluster_labels:", len(self.cluster_labels))
            if len(self.cluster_labels) != self.scaled_df.shape[0]:
                raise ValueError("Las dimensiones de cluster_labels y scaled_df no coinciden")
            return self.cluster_labels
        except Exception as e:
            print(f"Error en cluster_data: {str(e)}")
            raise

    def apply_pca(self, n_components=3):
        try:
            print("Ejecutando apply_pca")
            pca = PCA(n_components=n_components)
            principal_comp = pca.fit_transform(self.scaled_df)
            pca_df = pd.DataFrame(data=principal_comp, columns=['pca1', 'pca2', 'pca3'])
            pca_df['cluster'] = self.cluster_labels
            # Maneja NaN en pca_df
            pca_df = pca_df.fillna(0)
            print("Forma de pca_df:", pca_df.shape)
            return pca_df.to_dict(orient='records')
        except Exception as e:
            print(f"Error en apply_pca: {str(e)}")
            raise
            