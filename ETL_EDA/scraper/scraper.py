import traceback
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
from browser.settings import *
import time

def get_description_company(driver):
    company_info = {}
    resultado_soup=BeautifulSoup(driver.page_source, "lxml")
    description_company= resultado_soup.find(
        "div",
        {"class": "JobDetails_companyOverviewGrid__3t6b4"}
        )
    if description_company: 
        description_elements = description_company.find_all("div", class_="JobDetails_overviewItem__cAsry")

        for element in description_elements:
            label = element.find("span", class_="JobDetails_overviewItemLabel__KjFln").text.strip()
            value = element.find("div", class_="JobDetails_overviewItemValue__xn8EF").text.strip()
            company_info[label] = value
        print("datos de la empresa obtenidos")
    return company_info
    
    
def update_data(df, link, job_description_text, company_info):
    # Selecciona la fila del DataFrame que corresponde al link
    mask = df['Job Link'] == link
    
    # Utiliza loc para asignar valores a las columnas de la fila seleccionada
    df.loc[mask, 'Job Description'] = job_description_text
    df.loc[mask, 'Size'] = company_info.get('Tamaño', None)
    df.loc[mask, 'Founded'] = company_info.get('Fundado', None)
    df.loc[mask, 'Type of ownership'] = company_info.get('Tipo', None)
    df.loc[mask, 'Industry'] = company_info.get('Industria', None)
    df.loc[mask, 'Sector'] = company_info.get('Sector', None)
    df.loc[mask, 'Revenue'] = company_info.get('Ingresos', None)
    df.loc[mask, 'Status'] = 1  # Marca la fila como procesada
    #print(df[mask])
    return df

def get_description(driver):
    resultado_soup = BeautifulSoup(driver.page_source, "lxml")
    # Verificar si el elemento job_description_element existe
    job_description_element = resultado_soup.find(
                "div",
                {"class": "JobDetails_jobDescription__uW_fK JobDetails_blurDescription__vN7nh"}
            )
        
    if job_description_element is None:
        #se trata de una publicacion sin descripcion de la empresa 
        job_description_element = resultado_soup.find(
                "div",
                {"class": "JobDetails_jobDescription__uW_fK JobDetails_showHidden__C_FOA"}
                )
    return job_description_element

#Carga los links
df=pd.read_csv(r'datasets\Data-Science-Job_Listing.csv')

df['Status']= 0
df['Job Description']=None
df['Size']=None
df['Founded']=None
df['Type of ownership']=None
df['Industry']=None
df['Sector']=None
df['Revenue']=None

df=df[df['Status']== 0]
var=df[df['Status']== 0].shape[0]
print(var)

while var>0:
    count=0
    driver = create_local_driver(browser="chrome")
    for index, row in df.iterrows():
        try:
            link = row['Job Link']
            status= row['Status']
            if link and status==0:
                driver.get(link)
            else: 
                continue
            
            resultado= get_description(driver)
            
            if not resultado:
                driver.quit()
                time.sleep(10)
                break
            else: 
                print("descripcion obtenida")
            
            job_description_text = resultado.get_text(separator='\n').strip()

            # Optional filtering (uncomment if needed)
            filtered_text = '\n'.join([line for line in job_description_text.splitlines()
                                    if not line.startswith('Mostrar más')])

            
        
            company_description= get_description_company(driver)
            df=update_data(df, link,job_description_text,company_description) 
            time.sleep(10)
            count+=1

        except Exception as e:
            print("error: ",e)
            df.loc[df['Job Link'] == link, 'Status'] = 1
            continue
    df.to_csv(r'datasets/Data-Science-Job_Listing_completed.csv', index=False)
    var=df[df['Status']== 0].shape[0]
    print("Total procesados: ",count)
    print("Faltantes: ",var)
    
print(df.info())
df.to_csv(r'datasets/Data-Science-Job_Listing_completed.csv', index=False)
        
