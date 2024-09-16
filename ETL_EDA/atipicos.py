#Para trabajar los datos atípicos
from scipy.stats import zscore
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_liers(df, column, title='Without Outliers Visualization'):
    """
    Visualiza valores atípicos para una columna numérica utilizando un scatterplot.

    Parameters:
    df (DataFrame): El DataFrame que contiene los datos.
    column (str): El nombre de la columna numérica para analizar.
    title (str): El título del gráfico.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df[column], label='Data')
    # Scatterplot para valores atípicos
    sns.scatterplot(x=df.index, y=df[column], color='blue', alpha=0.6, label='Data Points')
    
    plt.title(title)
    plt.xlabel('Index')
    plt.ylabel(column)
    plt.grid(True)
    plt.legend()
    plt.show()

def detect_and_plot_outliers(df, column, threshold=4):
    """
    Detecta y visualiza valores atípicos en una columna numérica.

    Parameters:
    df (DataFrame): El DataFrame que contiene los datos.
    column (str): El nombre de la columna numérica para analizar.
    threshold (float): El umbral para la detección de valores atípicos.
    """
    # Calcular z-scores
    zscores = zscore(df[column].dropna())
    
    # Detectar outliers
    outliers = df[np.abs(zscores) > threshold]
    non_outliers = df[np.abs(zscores) <= threshold]
    
    # Imprimir información sobre los outliers
    print(f"Detected outliers in '{column}':")
    print(outliers[column])
    
    print(f'Data before removing outliers: {len(df[column])}')
    print(f'Data after removing outliers: {len(non_outliers[column])}')
    
    # Visualizar datos sin outliers
    plot_liers(non_outliers, column, title=f'Values without Outliers in {column}')