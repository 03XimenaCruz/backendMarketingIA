import pandas as pd
import numpy as np
import plotly.graph_objs as go

class VisualizationService:
    def __init__(self, df, scaled_df, cluster_labels):
        print("Inicializando VisualizationService")
        print("Columnas del DataFrame:", df.columns.tolist())
        print("Forma de scaled_df:", scaled_df.shape)
        print("Longitud de cluster_labels:", len(cluster_labels))
        self.df = df
        numeric_cols = df.select_dtypes(include=np.number).columns
        print("Columnas numéricas:", numeric_cols.tolist())
        self.scaled_df = pd.DataFrame(scaled_df, columns=numeric_cols)
        self.cluster_labels = cluster_labels
        self.sale_df_cluster = pd.concat([self.df, pd.DataFrame({'cluster': cluster_labels})], axis=1)
        print("Columnas de sale_df_cluster:", self.sale_df_cluster.columns.tolist())
        print("Valores NaN en SALES:", self.sale_df_cluster['SALES'].isna().sum())
        country_cols = [col for col in self.sale_df_cluster.columns if col.startswith('COUNTRY_')]
        for col in country_cols:
            print(f"Valores únicos en {col}:", self.sale_df_cluster[col].unique())
            print(f"Valores NaN en {col}:", self.sale_df_cluster[col].isna().sum())

    def get_sales_trend(self):
        try:
            print("Generando sales_trend")
            df = pd.read_csv('data/sales_data_sample.csv', encoding='latin1')
            df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')
            # Agrupa por día en lugar de por mes
            sales_trend = df.groupby(df['ORDERDATE'].dt.to_period('D'))['SALES'].sum().reset_index()
            sales_trend['ORDERDATE'] = sales_trend['ORDERDATE'].dt.to_timestamp()
            # Maneja NaN en SALES
            sales_trend['SALES'] = sales_trend['SALES'].fillna(0)
            print("Datos de sales_trend:", sales_trend.to_dict())
            return {
                'data': [
                    {
                        'type': 'scatter',
                        'mode': 'lines',
                        'x': sales_trend['ORDERDATE'].tolist(),  # Pasa fechas como datetime
                        'y': sales_trend['SALES'].tolist(),
                        'name': 'Ventas'
                    }
                ],
                'layout': {
                    'xaxis': {
                        'tickformat': '%b %Y'  # Formato "MMM YYYY"
                    },
                    'yaxis': {
                        'range': [0, 140000]  # Rango fijo como en la imagen
                    }
                }
            }
        except Exception as e:
            print(f"Error en get_sales_trend: {str(e)}")
            raise

    def get_country_bar(self):
        try:
            print("Generando country_bar")
            print("Columnas disponibles en sale_df_cluster:", self.sale_df_cluster.columns.tolist())
            # Limpia NaN en SALES antes del procesamiento
            self.sale_df_cluster['SALES'] = self.sale_df_cluster['SALES'].fillna(0)
            print("Valores NaN en SALES después de limpieza:", self.sale_df_cluster['SALES'].isna().sum())
            # Busca todas las columnas que empiecen con COUNTRY_
            country_cols = [col for col in self.sale_df_cluster.columns if col.startswith('COUNTRY_')]
            if not country_cols:
                raise ValueError("No se encontraron columnas dummy para COUNTRY")
            print("Columnas COUNTRY_ encontradas:", country_cols)
            # Calcula las ventas por país
            countries = []
            sales = []
            for country_col in country_cols:
                country_name = country_col.replace('COUNTRY_', '')
                # Limpia NaN en la columna dummy
                self.sale_df_cluster[country_col] = self.sale_df_cluster[country_col].fillna(0)
                print(f"Valores únicos en {country_col}:", self.sale_df_cluster[country_col].unique())
                # Suma las ventas donde country_col == 1
                country_sales = self.sale_df_cluster[self.sale_df_cluster[country_col] == 1]['SALES'].sum()
                if country_sales > 0:  # Solo incluye países con ventas
                    countries.append(country_name)
                    sales.append(country_sales)
            # Crea un DataFrame con los resultados
            country_sales_df = pd.DataFrame({'COUNTRY': countries, 'SALES': sales})
            print("Datos de country_sales_df:", country_sales_df.to_dict())
            # Verifica NaN en country_sales_df
            if country_sales_df['SALES'].isna().any() or country_sales_df['COUNTRY'].isna().any():
                raise ValueError("Valores NaN detectados en country_sales_df después de limpieza")
            # Define colores para cada país (usando la paleta de la imagen)
            country_colors = {
                'USA': '#1f77b4', 'Spain': '#ff0000', 'France': '#00ff00', 'Australia': '#9467bd',
                'UK': '#ff7f0e', 'Italy': '#2ca02c', 'Finland': '#d62728', 'Norway': '#98df8a',
                'Singapore': '#ff9896', 'Canada': '#aec7e8', 'Denmark': '#ffbb78', 'Germany': '#1f77b4',
                'Sweden': '#ff00ff', 'Austria': '#00ffff', 'Japan': '#ff0000', 'Belgium': '#00ff00',
                'Switzerland': '#ff7f0e', 'Philippines': '#2ca02c', 'Ireland': '#d62728'
            }
            colors = [country_colors.get(country, '#1f77b4') for country in country_sales_df['COUNTRY']]
            return {
                'data': [
                    {
                        'type': 'bar',
                        'orientation': 'h',  # Barras horizontales
                        'x': country_sales_df['SALES'].tolist(),
                        'y': country_sales_df['COUNTRY'].tolist(),
                        'marker': {'color': colors}
                    }
                ],
                'layout': {
                    'title': 'Ventas por País',
                    'xaxis': {'title': 'Ventas'},
                    'yaxis': {'title': 'País'},
                    'height': 600  # Ajusta la altura para mostrar todos los países
                }
            }
        except Exception as e:
            print(f"Error en get_country_bar: {str(e)}")
            raise

    def get_histograms(self, column):
        try:
            print(f"Generando histogramas para {column}")
            if column not in self.df.columns:
                raise ValueError(f"Columna {column} no encontrada")
            if not np.issubdtype(self.df[column].dtype, np.number):
                raise ValueError(f"Columna {column} no es numérica")
            histograms = []
            for cluster in range(5):
                cluster_data = self.sale_df_cluster[self.sale_df_cluster['cluster'] == cluster][column]
                # Maneja NaN en cluster_data
                cluster_data = cluster_data.dropna()
                if cluster_data.empty:
                    print(f"Advertencia: No hay datos válidos para {column} en clúster {cluster}")
                    continue
                histograms.append({
                    'data': [
                        {
                            'type': 'histogram',
                            'x': cluster_data.tolist(),
                            'name': f'Cluster {cluster}',
                            'marker': {'color': '#1f77b4'},  # Color azul como en la imagen
                            'opacity': 1.0  # Barras completamente opacas
                        }
                    ],
                    'layout': {
                        'title': f'{column} - Cluster {cluster}',  # Título como en la imagen
                        'xaxis': {'title': column},
                        'yaxis': {'title': 'Frecuencia'}
                    }
                })
            if not histograms:
                raise ValueError(f"No se generaron histogramas para {column}")
            return histograms
        except Exception as e:
            print(f"Error en get_histograms: {str(e)}")
            raise

    def get_correlation_heatmap(self):
        try:
            print("Generando correlation_heatmap")
            # Selecciona solo las columnas deseadas
            desired_cols = ['ORDERNUMBER', 'QUANTITYORDERED', 'PRICEEACH', 'ORDERLINENUMBER',
                            'SALES', 'QTR_ID', 'MONTH_ID', 'YEAR_ID']
            # Verifica si MSRP está presente y agrégalo si es así
            if 'MSRP' in self.df.columns:
                desired_cols.append('MSRP')
            # Filtra las columnas que existen en el DataFrame
            available_cols = [col for col in desired_cols if col in self.df.columns]
            if not available_cols:
                raise ValueError("No se encontraron columnas numéricas deseadas para la correlación")
            print("Columnas usadas para la correlación:", available_cols)
            # Calcula la matriz de correlación
            corr_matrix = self.df[available_cols].corr()
            # Maneja NaN en corr_matrix
            corr_matrix = corr_matrix.fillna(0)
            print("Matriz de correlación:", corr_matrix.values.tolist())
            # Crea una matriz de texto para las anotaciones (valores redondeados a 2 decimales)
            text_matrix = [[f"{val:.2f}" for val in row] for row in corr_matrix.values]
            return {
                'data': [
                    {
                        'type': 'heatmap',
                        'z': corr_matrix.values.tolist(),
                        'x': available_cols,
                        'y': available_cols,
                        'colorscale': 'RdBu',  # Paleta divergente rojo-azul
                        'text': text_matrix,  # Valores como texto
                        'hoverinfo': 'text',
                        'showscale': True
                    }
                ],
                'layout': {
                    'title': 'Matriz de Correlación',
                    'xaxis': {'title': 'Variables'},
                    'yaxis': {'title': 'Variables'},
                    'width': 600,
                    'height': 600
                }
            }
        except Exception as e:
            print(f"Error en get_correlation_heatmap: {str(e)}")
            raise

    def get_pca_scatter(self):
        try:
            print("Generando pca_scatter")
            pca_df = pd.DataFrame(self.scaled_df, columns=self.df.select_dtypes(include=np.number).columns)
            pca_df['cluster'] = self.cluster_labels
            # Maneja NaN en pca_df
            pca_df = pca_df.fillna(0)
            print("Primeras filas de pca_df:", pca_df.head().to_dict())
            return {
                'data': [
                    {
                        'type': 'scatter3d',
                        'x': pca_df.iloc[:, 0].tolist(),
                        'y': pca_df.iloc[:, 1].tolist(),
                        'z': pca_df.iloc[:, 2].tolist(),
                        'mode': 'markers',
                        'marker': {
                            'color': pca_df['cluster'].tolist(),
                            'colorscale': 'Jet',  # Paleta de morado a amarillo
                            'size': 2,  # Tamaño más pequeño como en la imagen
                            'colorbar': {'title': 'cluster'}  # Etiqueta para la barra de color
                        }
                    }
                ],
                'layout': {
                    'scene': {
                        'xaxis': {
                            'title': 'pca1',
                            'autorange': 'reversed'  # Invierte el eje X
                        },
                        'yaxis': {
                            'title': 'pca2',
                            'autorange': 'reversed'  # Invierte el eje Y
                        },
                        'zaxis': {
                            'title': 'pca3',
                            'autorange': 'reversed'  # Invierte el eje Z
                        }
                    }
                }
            }
        except Exception as e:
            print(f"Error en get_pca_scatter: {str(e)}")
            raise