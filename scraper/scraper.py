import traceback
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import pandas as pd
#import request
from browser.settings import *
import time
import os 

#Carga los links
df=pd.read_csv(r'datasets\Data-Science-Job_Listing.csv')
lista_de_links = df['Job Link'].tolist()
#print(lista_de_links)

driver = create_local_driver(browser="chrome")
for link in lista_de_links:
    try:
        driver.get(link)
        os.system('pause')
        time.sleep(10)
        resultado_soup = BeautifulSoup(driver.page_source, "lxml")
        resultado = resultado_soup.find( "div",
                                {"class": "JobDetails_jobDescriptionWrapper___tqxc JobDetails_jobDetailsSectionContainer__o_x6Z JobDetails_paddingTopReset__IIrci"},)
        if resultado:
            print(resultado)
        else: print("resultado no encontrado")
        exit(0)
    except Exception as e:
        print(e)
        exit(0)