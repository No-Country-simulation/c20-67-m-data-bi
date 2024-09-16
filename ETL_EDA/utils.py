import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import re 
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk

#Funciones utiles para tratamiento de datos

def plot_top_n_categories(df, column, n=20):
    top_n = df[column].value_counts().nlargest(n)
    plt.figure(figsize=(12, 8))
    sns.barplot(y=top_n.index, x=top_n.values, palette='viridis')
    plt.title(f'Top {n} most common {column}')
    plt.ylabel(column)
    plt.xlabel('Count')
    plt.gca().set_yticklabels(top_n.index, rotation=0, ha='right')
    return plt.show()

def convertir_salario_por_hora(salario):
    """Convierte un salario por hora a anual y obtiene los valores mínimos y máximos."""
    if pd.isna(salario):
        return 0, 0

    salario = str(salario).strip()

    # Eliminar texto que no es necesario
    salario_limpio = re.sub(r'Per Hour.*', '', salario).strip()
    partes = salario_limpio.split('-')

    if len(partes) == 2:
        try:
            min_salario_hora = float(partes[0].replace('$', '').replace(',', ''))
            max_salario_hora = float(partes[1].replace('$', '').replace(',', ''))
        except ValueError:
            return 0, 0
    elif len(partes) == 1:
        try:
            min_salario_hora = max_salario_hora = float(partes[0].replace('$', '').replace(',', ''))
        except ValueError:
            return 0, 0
    else:
        return 0, 0

    # Convertir a anual
    min_salario_anual = min_salario_hora * 2080
    max_salario_anual = max_salario_hora * 2080
    return min_salario_anual, max_salario_anual


def clear_salary(salario):
    """Limpia un valor de salario para obtener los números mínimos y máximos."""
    if pd.isna(salario):
        return 0, 0

    salario = str(salario).strip()

    # Eliminar texto entre paréntesis y caracteres no numéricos excepto guiones
    salario_limpio = re.sub(r'\(.*\)', '', salario)  # Elimina texto en paréntesis
    salario_limpio = re.sub(r'[^\dKk-]', '', salario_limpio)  # Elimina caracteres no numéricos excepto guiones

    # Reemplazar el sufijo 'K' para manejar los valores en miles
    salario_limpio = salario_limpio.replace('K', '000').replace('k', '000')

    # Dividir el string en dos usando el guion como separador
    partes = salario_limpio.split('-')

    if len(partes) == 2:
        try:
            minimo = int(partes[0])
            maximo = int(partes[1])
        except ValueError:
            return 0, 0
    elif len(partes) == 1:
        try:
            minimo = maximo = int(partes[0])
        except ValueError:
            return 0, 0
    else:
        return 0, 0

    return minimo, maximo

def extraer_salarios(df, columna_salario):
    """Aplica las funciones de conversión de salario al DataFrame y calcula el salario promedio."""
    df[['min_salary', 'max_salary']] = df[columna_salario].apply(
        lambda x: pd.Series(
            convertir_salario_por_hora(x) if 'Per Hour' in str(x) else clear_salary(x)
        )
    )

    # Calcular el promedio del salario
    df['avg_salary'] = (df['min_salary'] + df['max_salary']) / 2

    return df

def split_location(location):
    try:
        if ',' in location:
            city, state = location.split(',', 1)
            return city.strip(), state.strip()
        else:
            return location, location
    except Exception as e:
        print(f"Error processing location {location}: {e}")
        return location, location

def title_simplifier(title):
    title = title.lower()

    if "front-end" in title:
        return "front-end developer"
    elif "backend" in title or "back-end" in title:
        return "backend developer"
    elif "full-stack" in title:
        return "full-stack developer"
    if "data scientist" in title or "data sciences" in title or "data science" in title or "scientist" in title:
        if "senior manager" in title or "principal" in title:
            return "senior data scientist"
        else:
            return "data scientist"
    elif "data engineer" in title:
        return "data engineer"
    elif "data analyst" in title or "analyst" in title or "analytics" in title:
        return "data analyst"
    elif "machine learning" in title:
        return "machine learning engineer"
    elif "devops" in title:
        return "devops engineer"
    elif "cloud" in title:
        return "cloud engineer"
    elif "qa" in title:
        return "qa engineer"
    elif "robotics" in title:
        return "robotics engineer"
    elif "software engineer" in title:
        if "front-end" in title:
            return "software engineer - front-end"
        elif "backend" in title:
            return "software engineer - backend"
        else:
            return "software engineer"
    else:
        return title


def seniority(title):
    title = title.lower()

    if "senior" in title or "sr" in title or "lead" in title or "principal" in title or "iii" in title:
        return "senior"
    elif "ii" in title or "mid" in title or "mgr" in title:
        return "semi-senior"
    elif "junior" in title or "jr" in title or "associate" in title or "i" in title:
        return "junior"
    else:
        return "unspecified"


def extract_key_info(text):
    """Extracts key information from a job description text.
    Args:
        text (str): The job description text.
    Returns:
        dict: A dictionary containing extracted skills, responsibilities, and requirements.
    """

    # Ensure the input is a string
    if not isinstance(text, str):
        return {
            'skills': [],
            'responsibilities': [],
            'requirements': []
        }

    # Load the spaCy model (ensure it's installed)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)


    # Define keywords for each section
    section_keywords = {
        'skills': ['skill', 'ability', 'expertise', 'proficiency', 'knowledge'],
        'responsibilities': ['responsibility', 'task', 'duty', 'deliverable', 'outcome'],
        'requirements': ['requirement', 'qualifications', 'experience', 'education', 'certification']
    }

    # Extract sections based on keywords and sentence structure
    sections = {
        'skills': [],
        'responsibilities': [],
        'requirements': []
    }
    for sent in doc.sents:
        for section, keywords in section_keywords.items():
            if any(keyword in sent.text.lower() for keyword in keywords):
                sections[section].append(sent)
                break
    # Clean up extracted sections and extract text
    for section in sections:
        sections[section] = [sent.text.strip().replace('\r\n', ' ').replace('\n', ' ') for sent in sections[section]]

    return sections

def clean_skills(text, custom_keywords=None):
    """Extrae palabras clave de habilidades de un texto.
    Args:
        text (str): El texto a analizar.
        custom_keywords (list, optional): Lista de palabras clave personalizadas.
    Returns:
        set: Conjunto de palabras clave extraídas.
    """
    if isinstance(text, float) or text is None:
        return ''  # Devolver una cadena vacía si no es una cadena

    if isinstance(text, list):
        text = ' '.join(text)  # Convertir lista en string
    elif not isinstance(text, str):
        return ''  # Devolver una cadena vacía si no es una cadena

    nltk.download('stopwords')
    nltk.download('wordnet')

    # Cargar el modelo spaCy
    nlp = spacy.load("en_core_web_sm")

    # Preprocesamiento del texto
    doc = nlp(text.lower())

    # Eliminar stop words y aplicar lematización
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token.text) for token in doc if token.text not in stop_words]

    # Combinar keywords personalizadas con las predefinidas
    keywords = {
        "machine learning programming", "statistical", "SAS", "Python", "R",
        'MailChimp', 'Public speaking', 'User acceptance testing', 'Groovy', 'SDLC',
        'C', 'Writing skills', 'Performance testing', 'Mechanical engineering', 
        'SQL', 'MySql', 'Mariadb', 'Test automation', 'PowerBI', 'Contracts', 
        '.NET', 'SaaS', 'System testing', 'SFTP', 'Asana', 'A/B testing','Looker studio','Data Studio','JavaScript'
        }
    if custom_keywords:
        keywords.update(custom_keywords)

    # Extraer frases y palabras que coincidan con las keywords
    extracted_skills = set()
    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens) + 1):
            phrase = ' '.join(tokens[i:j])
            if phrase in keywords:
                extracted_skills.add(phrase)

    return extracted_skills

def clean_column_names(df):
    """
    Limpia los nombres de las columnas del DataFrame, convirtiéndolos a minúsculas y
    reemplazando los espacios con guiones bajos para darles formato snake_case.
    Args:
    df (pd.DataFrame): El DataFrame cuyas columnas se desean limpiar.
    Returns:
    pd.DataFrame: El DataFrame con los nombres de las columnas limpiados.
    """
    # Estandarizar columnas
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    return df

def null_duplicates_review(df, nombre_df='DataFrame'):
    """
    Verifica y muestra el porcentaje de valores nulos y el número de duplicados en un DataFrame.
    Args:
    df (pd.DataFrame): El DataFrame a analizar.
    nombre_df (str): Nombre del DataFrame para identificación en los resultados. Por defecto es 'DataFrame'.
    Returns:
    None: Imprime los resultados en consola.
    """
    # Verificar valores nulos
    nulls = round(df.isnull().sum() / df.shape[0] * 100, 2)
    print(f"Valores ausentes en {nombre_df}:\n{nulls.to_frame(name='Valores ausentes (%)')}\n")

    # Verificar duplicados
    duplicates = df.duplicated().sum()
    print(f"Total duplicados en {nombre_df}: {duplicates}\n")

def capitalize_column(df, column_name):
    """
    Convierte la primera letra de cada palabra en mayúscula y el resto en minúscula.
    Args:
    df (pd.DataFrame): El DataFrame a analizar.
    column_name: Nombre de la columna 
    Returns:
    None: Imprime los resultados en consola.
    """
    df[column_name] = df[column_name].str.title()
    return df

def plot_outliers(df, column, title='Outliers Visualization'):
    """
    Visualiza valores atípicos para una columna numérica utilizando un scatterplot.
    Parameters:
    df (DataFrame): El DataFrame que contiene los datos.
    column (str): El nombre de la columna numérica para analizar.
    title (str): El título del gráfico.
    """
    plt.figure(figsize=(12, 6))

    # Scatterplot
    sns.scatterplot(x=df.index, y=df[column], color='blue', alpha=0.6)

    plt.title(title)
    plt.xlabel('Index')
    plt.ylabel(column)
    plt.grid(True)
    plt.show()