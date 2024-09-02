from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service

firefox_preferences = webdriver.FirefoxProfile()
#NO LEVANTA EL DIALOGO PARA PREGUNTAR SI QUIERE DESCARGAR. SOLO SE APLICA A TEXTO Y PDF (BUSCAR OTROS)
firefox_preferences.set_preference("browser.helperApps.neverAsk.saveToDisk","text/plain,application/pdf")
firefox_preferences.set_preference("browser.download.manager.showWhenStarting", False)
#SETEA EL LUGAR DONDE VA A GUARDAR
firefox_preferences.set_preference("browser.download.dir","")
firefox_preferences.set_preference("browser.download.folderList",2)
firefox_preferences.set_preference("pdfjs.disabled",True)

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument("start-maximized")
firefox_options.add_argument("enable-automation")
firefox_options.add_argument("--headless")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-infobars")
firefox_options.add_argument("--disable-dev-shm-usage")
firefox_options.add_argument("--disable-browser-side-navigation")
firefox_options.add_argument("--disable-gpu")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("enable-automation")
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-browser-side-navigation")
chrome_options.add_argument("--disable-gpu")

def create_local_driver(browser='chrome'):
    driver = None
    
    if browser == 'chrome':
        # driver = webdriver.Chrome(executable_path=ChromeDriverManager(version="114.0.5735.90").install(), options=chrome_options)
        #driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
        service = Service(executable_path='./chromedriver')
        driver = webdriver.Chrome(service= service, options=chrome_options)
    driver.implicitly_wait(30)
    return driver

capabilities_moz = { \
    'browserName': 'firefox',
    'marionette': True,
    'acceptInsecureCerts': True,
    'moz:firefoxOptions': { \
      'args': [],
      'prefs': {
        'browser.download.dir': '',
        'browser.helperApps.neverAsk.saveToDisk': 'application/octet-stream,application/pdf', 
        'browser.download.useDownloadDir': True, 
        'browser.download.manager.showWhenStarting': False, 
        'browser.download.animateNotifications': False, 
        'browser.safebrowsing.downloads.enabled': False, 
        'browser.download.folderList': 2,
        'pdfjs.disabled': True
      }
    }
  }

