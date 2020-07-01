from bs4 import BeautifulSoup
import pandas as pd
import time
import chromeConfig as chrome
import config

ruts = pd.read_csv('../csv/compilado_ruts_unicos.txt', sep = '\n', header = None)


driver = chrome.driver()

data = pd.DataFrame()

for r in range(ruts.shape[0]):
    try:
        driver.get(config.url_multa)
        driver.find_element_by_xpath('//*[@id="tbxRut"]').send_keys(ruts[0][r])
        driver.find_element_by_xpath('//*[@id="btnConsulta"]').click()
        time.sleep(2)

        aux = pd.DataFrame()
        while chrome.check_exists_by_css_selector(driver, '#grd__ctl1 > tfoot > tr > td > a:nth-child(6)'):
            soup = BeautifulSoup(driver.page_source, "html.parser")
            aux = aux.append(pd.read_html(str(soup))[0].iloc[:-1])
            driver.find_element_by_css_selector('#grd__ctl1 > tfoot > tr > td > a:nth-child(6)').click()
            time.sleep(1.5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        aux = aux.append(pd.read_html(str(soup))[0].iloc[:-1])
        aux['RUT'] = ruts[0][r]
        data = data.append(aux)
        
    except:
        pass
    print('Iteración '+str(r+1)+' de %s'%ruts.shape[0]+': %s'%ruts[0][r]+' completada')

driver.close()

data.to_csv('../adicionales/compilado_ruts_unicos_multas.csv', encoding = 'utf-8', index = False)