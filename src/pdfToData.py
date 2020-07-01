import os
from glob import glob
import tabula
import pandas as pd

#Crea el folder donde se irán guardando los archivos convertidos
if not os.path.exists('../csv'):
    os.makedirs('../csv')

files = glob('../pdfs/*reducción_jornada.pdf')

for file in files:
    tabula.convert_into(file,
                        file.replace('pdfs','csv').replace('pdf','csv'),
                        output_format='csv', pages='all')
    print('%s convertido exitosamente'%file)

#Convertimos cada archivo particular en un compilado de todos ellos
csv = glob('../csv/*reducción_jornada.csv')
dataset = pd.DataFrame()

for c in range(len(csv)):
    aux = pd.read_csv(csv[c], encoding = 'utf-8')
    dataset = dataset.append(aux)
    print(csv[c])

#Exportamos la información compilada
dataset['RUT'] = dataset['RUT Empleador'].astype(str) + '-' + dataset['DV Empleador']
dataset.to_csv('../csv/compilado_reducción_jornada.csv', encoding = 'utf-8', index = False)

#Exportamos los ruts únicos para consultar
pd.DataFrame(dataset['RUT'].unique()).to_csv('../csv/compilado_ruts_unicos.txt', sep = '\n', index = False, header=False)