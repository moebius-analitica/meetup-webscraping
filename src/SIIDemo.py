import base64
import requests
from bs4 import BeautifulSoup

#Datos de ejemplo
rut = '60901000'
dv = '2'

#Request al SII-captcha
captcha_req = requests.post("https://zeus.sii.cl/cvc_cgi/stc/CViewCaptcha.cgi",data={'oper':'0'})
respuesta = captcha_req.json()
#Se obtiene el string que contiene la información del captcha
txtCaptcha= respuesta['txtCaptcha']

#Decodificación del texto anterior
code = base64.b64decode(txtCaptcha)[36:40]

#Petición al SII, con captcha resuelto
consulta_sii = requests.post("https://zeus.sii.cl/cvc_cgi/stc/getstc",data={'RUT':rut,'DV':dv.upper(),'PRG':'STC','OPC':'NOR','txt_code':code,'txt_captcha':txtCaptcha})

#Parseo de los datos
datos = BeautifulSoup(consulta_sii.text,"html.parser")

#Obtención de la razón social
razon_social= consulta_sii.text.split("n Social&nbsp;:")
razon_social = razon_social[1].split("</div>")
razon_social = razon_social[1][74:].strip()

#Inicio de actividades
inicio_actividades =datos.find_all("span")
inicio_actividades = consulta_sii.text.split("Fecha de Inicio de Actividades: ")
if len(inicio_actividades)>1:    
    inicio_actividades = inicio_actividades[1][0:10]
else:
    inicio_actividades = None

print(razon_social)
print(inicio_actividades)