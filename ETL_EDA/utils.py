import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import re 
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

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


def clear_salary(salario):
    """Limpia un valor de salario para obtener los números mínimos y máximos."""
    # Verificar si el salario es nulo
    if pd.isna(salario):
        # Retorna valores por defecto para nulos
        return 0, 0
    
    # Elimina caracteres no numéricos excepto guiones, y elimina todo el texto entre paréntesis
    salario_limpio = re.sub(r'[^\dKk-]', '', salario)
    
    # Quita el sufijo 'K' para manejar los valores en miles
    salario_limpio = salario_limpio.replace('K', '000').replace('k', '000')
    
    # Divide el string en dos usando el guion como separador
    partes = salario_limpio.split('-')

    # Si hay dos partes, convierte ambas a enteros
    if len(partes) == 2:
        minimo, maximo = map(int, partes)
    elif len(partes) == 1:
        # Si solo hay una parte, usa el mismo valor para mínimo y máximo
        minimo = maximo = int(partes[0])
    else:
        # Si el formato no es válido, devuelve valores por defecto (0, 0)
        minimo, maximo = 0, 0
    
    return minimo, maximo

def extraer_salarios(df, columna_salario):
    # Aplicar la función de limpieza a la columna de salarios y expandir en dos columnas usando pd.Series
    df[['min_salary', 'max_salary']] = df[columna_salario].apply(lambda x: pd.Series(clear_salary(x)))

    # Calcular el promedio del salario
    df['avg_salary'] = (df['min_salary'] + df['max_salary']) / 2

    return df

def title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'data analyst'
    elif 'machine learning' in title.lower():
        return 'machine learning engineer'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    elif 'software engineer' in title.lower() or 'software engineers' in title.lower():
        return 'software engineer'
    else:
        return title.lower()
    
def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'sr' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
            return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower():
        return 'jr'
    else:
        return 'na'
    
'''Limpieza de Skills'''
nlp = spacy.load("en_core_web_sm")

# Función para extraer secciones clave del texto
def extract_key_info(text):

    # Asegurarse de que el input es un string
    if not isinstance(text, str):
        return {
            'skills': [],
            'responsibilities': [],
            'requirements': []
        }
    
    doc = nlp(text)
    skills = []
    responsibilities = []
    requirements = []
    
    # Detectar secciones claves basadas en encabezados comunes
    sections = {
        'skills': ['Skills', 'Skilled', 'Expert', 'Proficient'],
        'responsibilities': ['Responsibilities', 'Responsibility'],
        'requirements': ['Requirements', 'Required', 'Minimum Requirements', 'Preferred Requirements']
    }
    
    # Dividir el texto en líneas
    lines = text.split('\n')
    
    # Variables auxiliares para determinar la sección actual
    current_section = None
    
    for line in lines:
        # Limpiar la línea
        line = line.strip()
        if not line:
            continue
        
        # Detectar la sección actual
        for section, keywords in sections.items():
            if any(keyword in line for keyword in keywords):
                current_section = section
                break
        
        # Agregar líneas relevantes a la sección correspondiente
        if current_section == 'skills' and line and line not in sections['skills']:
            skills.append(line)
        elif current_section == 'responsibilities' and line and line not in sections['responsibilities']:
            responsibilities.append(line)
        elif current_section == 'requirements' and line and line not in sections['requirements']:
            requirements.append(line)
    
    return {
        'skills': skills,
        'responsibilities': responsibilities,
        'requirements': requirements
    }

def clean_skills(text):

    # Lista de palabras clave específicas que queremos extraer como habilidades
    keywords = {
    "machine learning programming", "statistical", "SAS", "Python", "R",
    'MailChimp', 'Public speaking', 'User acceptance testing', 'Groovy', 'SDLC',
    'C', 'Writing skills', 'Performance testing', 'Mechanical engineering', 
    'SQL', 'MySql', 'Mariadb', 'Test automation', 'PowerBI', 'Contracts', 
    '.NET', 'SaaS', 'System testing', 'SFTP', 'Asana', 'A/B testing','Looker studio','Data Studio','JavaScript'
    }

    if isinstance(text, float) or text is None:
        return ''  # Devolver una cadena vacía si no es una cadena

    if isinstance(text, list):
        text = ' '.join(text)  # Convertir lista en string
    elif not isinstance(text, str):
        return ''  # Devolver una cadena vacía si no es una cadena

    # Procesar el texto con SpaCy
    doc = nlp(text.lower())
    
    # Extraer frases o palabras que coincidan con nuestras keywords
    extracted_skills = set()
    
    # Usar frases y tokens lematizados para coincidencia más flexible
    for token in doc:
        lemma = token.lemma_
        # Comparar cada lematización y combinación de palabras con las keywords
        if lemma in keywords:
            extracted_skills.add(lemma)
            
    # Revisar combinaciones de 2 y 3 palabras como n-gramas
    for i in range(len(doc)):
        for j in range(i + 1, len(doc) + 1):
            phrase = ' '.join([doc[k].lemma_ for k in range(i, j)])
            if phrase in keywords:
                extracted_skills.add(phrase)

    # Unir las palabras clave encontradas en un string limpio
    return ', '.join(extracted_skills)
