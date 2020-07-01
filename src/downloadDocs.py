import requests
from bs4 import BeautifulSoup
import wget
import os
import config


#Crea el folder donde se irán guardando los archivos descargados
if not os.path.exists('../pdfs'):
    os.makedirs('../pdfs')

#Link de referencia para acceder al sitio web
link = config.url_base + 'w3-article-118613.html'

#Se realiza el request a la webpage para ingresar al codigo fuente
r = requests.get(link)
if r.status_code == 200:
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, features='html.parser')

else:
    print('Hubo un problema al ingresar la página: error %s'%r.status_code)


#Elementos donde se encuentran los enlaces de los archivos y las fechas de estos
elements = soup.find('div',{'class':'cid-912 aid-118613'}).find_all('p')

#Objetos donde se guardarán los atributos necesarios para almacenar los archivos localmente
dates = []; files = []; typo = []


for e in range(len(elements)):
    if (e % 2) != 0:
        files.append([x['href'] for x in elements[e].find_all('a')])
        typo.append([x['alt'] for x in elements[e].find_all('img')])
    else:
        dates.append(elements[e].text.split('Publicación ')[1].strip(':'))

#Comienzo de descarga de los archivos
for x in range(len(dates)):
    for y in range(len(files[x])):
        if 'suspensión' in typo[x][y]:
            wget.download(config.url_base + files[x][y], '../pdfs/'+ dates[x].replace(' de ','-')+'_suspensión_contrato.pdf')
        else:
            wget.download(config.url_base + files[x][y], '../pdfs/'+ dates[x].replace(' de ','-')+'_reducción_jornada.pdf')
    print('%s descargado exitosamente'%dates[x])