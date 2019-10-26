import pandas as pd
import lxml
import json
import requests
import re
from datetime import date
from datetime import datetime

#Ajustes de Datas Cotações
def CoinDate(date):
  date_clock = date[11:20:]
  date_ajust = date[:10:]
  date_day = date_ajust[8:10:]
  date_year = date_ajust[:4:]
  date_month_test = date_ajust[5:7:]
  date_date = '{}/{}/{} {}'.format(date_day, date_month_test, date_year, date_clock)

  return date_date

#===============================
#Web Scraping
#===============================
#Cotação json

lista = requests.get('https://economia.awesomeapi.com.br/all')

cotation = json.loads(lista.text)

dollar_name = cotation['USD']['name']
doll = cotation['USD']['high']
dollarsplit = doll.split(',')
dollar = dollarsplit[0] + '.' + dollarsplit[1]
dollar_date = cotation['USD']['create_date']
dollar_date = CoinDate(dollar_date)

dollar_cad_name = cotation['CAD']['name']
dollar_cad = cotation['CAD']['high']
dollar_cad_date = cotation['CAD']['create_date']
dollar_cad_date = CoinDate(dollar_cad_date)

dollar_aus_name = cotation['AUD']['name']
dollar_aus = cotation['AUD']['high']
dollar_aus_date = cotation['USD']['create_date']
dollar_aus_date = CoinDate(dollar_aus_date)

bitcoin_name = cotation['BTC']['name']
bitcoin = cotation['BTC']['high']
bitcoin_date = cotation['BTC']['create_date']
bitcoin_date = CoinDate(bitcoin_date)
btc = bitcoin
#btc = float(bitcoin)

litcoin_name = cotation['LTC']['name']
litcoin = cotation['LTC']['high']
litcoin_date = cotation['LTC']['create_date']
litcoin_date = CoinDate(litcoin_date)
ltc = litcoin
#ltc = float(litcoin)

euro_name = cotation['EUR']['name']
euro = cotation['EUR']['high']
euro_date = cotation['EUR']['create_date']
euro_date = CoinDate(euro_date)

libra_name = cotation['GBP']['name']
libra = cotation['GBP']['high']
libra_date = cotation['GBP']['create_date']
libra_date = CoinDate(libra_date)

peso_name = cotation['ARS']['name']
peso = cotation['ARS']['high']
peso_date = cotation['ARS']['create_date']
peso_date = CoinDate(peso_date)

iene_name = cotation['JPY']['name']
iene = cotation['JPY']['high']
iene_date = cotation['JPY']['create_date']
iene_date = CoinDate(iene_date)

dados = [ [dollar_name, dollar, dollar_date],
          [dollar_cad_name, dollar_cad, dollar_cad_date],
          [dollar_aus_name, dollar_aus, dollar_aus_date],
          [bitcoin_name, btc, bitcoin_date],
          [litcoin_name, ltc, litcoin_date],
          [euro_name, euro, euro_date],
          [libra_name, libra, libra_date],
          [peso_name, peso, peso_date],
          [iene_name, iene, iene_date]
        ]

header = ['   Moeda         ', '     Valor            ', '    Data Cotação        ']

df = pd.DataFrame(data=dados, columns=header)


#===============================
#Relógio Calendário
#===============================

hj = date.today()

data_em_texto = hj.strftime('%d/%m/%Y')

hj = date.today()
dias = ('Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado', 'Domingo')
mes = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')

days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
month_s = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')

day_week = dias[hj.weekday()]
days_week = days[hj.weekday()]
day = data_em_texto[:2:]
year = data_em_texto[6:10:]
month_test = data_em_texto[3:5:]
month = mes[int(month_test[1]) - 1]
months = month_s[int(month_test[1]) - 1]


#===============================
#FIPE_1
#===============================
url = 'http://fipeapi.appspot.com/api/1/carros/marcas.json'
r = requests.get(url)
fip_all = json.loads(r.text)
id_mark, mark = [], []

for i in range(len(fip_all)):
  id_mark.append([fip_all[i]['name'], fip_all[i]['id']])
  #print(fip_all[i]['name'], fip_all[i]['id'])
  mark.append([fip_all[i]['name'], fip_all[i]['id']])

#===============================
#FIPE_2
#===============================

def name_car(var, car_type):
  print('====',var, car_type)

  id_code = ''
  for a in var:
    if a[0] == car_type:
      id_code = a[1]

  url = 'http://fipeapi.appspot.com/api/1/carros/veiculos/' + str(id_code) + '.json' #id
  r = requests.get(url)
  fip_all2 = json.loads(r.text)

  name_car_fipe = []
  for a in range(len(fip_all2)):
    name_car_fipe.append(fip_all2[a]['fipe_name'])

  name_car_fipe.append(id_code)
    
  return name_car_fipe

#===============================
#FIPE_3
#===============================

def year_car(code_car, car_name, id_code):
  print('tttttttt',code_car, car_name)

  url = 'http://fipeapi.appspot.com/api/1/carros/veiculos/' + str(id_code) + '.json' #id
  r = requests.get(url)
  fip_all2 = json.loads(r.text)

  select_car = []

  for a in range(len(fip_all2)):
    searched_name = re.search(car_name, fip_all2[a]['fipe_name'])

    if searched_name != None:
      print('Entrou!!!')
      if fip_all2[a]['fipe_name'] == car_name:
        select_car.append(fip_all2[a])
      
  id_value = []
  for a in range(len(select_car)):
    id_value.append(select_car[a]['id'])
    
  year_car = []
  for i in id_value:

    url = 'http://fipeapi.appspot.com/api/1/carros/veiculo/' + str(id_code) + '/' + str(i) + '.json'
    r = requests.get(url)
    fip_all3 = json.loads(r.text)
    
  for a in range(len(fip_all3)):
    year_car.append(fip_all3[a]['id'])

  year_date = []
  print('\n|  ANOS DISPONÍVEIS PARA PESQUISA  |')
  for a in year_car:
    print(a[:4:])
    year_date.append(a[:4:])

  print(year_date)

  return year_date

#===============================
#FIPE_4
#===============================

def final_fipe(car_name, id_code, car_date):
  url = 'http://fipeapi.appspot.com/api/1/carros/veiculos/' + str(id_code) + '.json'  # id
  r = requests.get(url)
  fip_all2 = json.loads(r.text)

  select_car = []

  for a in range(len(fip_all2)):
    if fip_all2[a]['fipe_name'] == car_name:
      select_car.append(fip_all2[a])

  id_value = []
  for a in range(len(select_car)):
    id_value.append(select_car[a]['id'])

  year = car_date + '-1'

  fip, lista_car, table, table_fip = [], [], [], []
  for i in id_value:

    url = 'http://fipeapi.appspot.com/api/1/carros/veiculo/' + str(id_code) + '/' + i + '.json'
    r = requests.get(url)
    fip_all3 = json.loads(r.text)
    for a in fip_all3:
      date = a['id']

      searched_date = re.search(year, date)

      if searched_date != None:
        url2 = 'http://fipeapi.appspot.com/api/1/carros/veiculo/' + str(id_code) + '/' + str(i) + '/' + year + '.json'
        r = requests.get(url2)
        fip = json.loads(r.text)
        table.append(fip)

  for a in range(len(table)):
    table_fip.append(
      [table[a]['marca'], table[a]['name'], table[a]['combustivel'], table[a]['preco'], table[a]['referencia']])

    print('\n')
  df = pd.DataFrame(data=table_fip, columns=['MARCA', 'MODELO', 'COMBUSTÍVEL', 'PREÇO', 'REFERENCIA'])

  return df