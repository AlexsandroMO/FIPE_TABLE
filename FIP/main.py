#Created by:  Alexsandro Monteiro
#Date:        26/07/2019
#Site for Tests Python / Flask
#Fipe Table Consult

#Python any Where
#https://www.pythonanywhere.com/user/AlexsandroMO/
#pip install flask

from flask import Flask, render_template, url_for, request,send_from_directory
import Progpy
import xlrd

#==================================
app = Flask(__name__)

Ass = 'A.M.O COTACÕES'
df = Progpy.df
day_week = Progpy.day_week
days_week = Progpy.days_week
day = Progpy.day
months = Progpy.months
month = Progpy.month
year = Progpy.year
hj = Progpy.hj

class ItensCar():
  def __init__(self, var, code_car, car_name_model, car_name_brand, id_code):
    self.var = var
    self.code_car = code_car
    self.car_name_model = car_name_model
    self.car_name_brand = car_name_brand
    self.id_code = id_code

@app.route('/')
@app.route('/home_us')
def home_us():
  return render_template('home_us.html')

@app.route('/resultfip')
def resultfip():
  return render_template('resultfip.html')

@app.route('/login_us')
def login_us():
  return render_template('login_us.html')

@app.route("/cotation_us")
def cotation_us():
  return render_template('cotation_us.html')

@app.route('/resultcotation', methods = ['POST', 'GET'])
def resultcotation():

  if request.method == 'POST':
    resultcotation = request.form
    var_modeda = resultcotation['dolar-real']
    tipo_moeda = resultcotation['moeda']

    print(resultcotation)
    print('>>: ', var_modeda)
    print('>>: ', tipo_moeda)

    if tipo_moeda == 'dolar':
      valor = float(Progpy.dollar) * float(var_modeda)
      var = '%.2f' % valor
      unidade = 'Reais'
      uf = 'R$'

    if tipo_moeda == 'real':
      valor = float(var_modeda) / float(Progpy.dollar)
      var = '%.2f' % valor
      unidade = 'Dolares'
      uf = '$'

    if var_modeda == '' and tipo_moeda == '':
      return f"""
        <p>Atenção, Todos os campos precisam ser preenchidos... :( </p>
        <br>
        <br>
        <br>
        <p><a href="/cotation"><img src="https://image.flaticon.com/icons/png/512/54/54906.png" alt="some text" width=40 height=40></p>

        """

    return render_template("resultcotation.html", title='Python_Flask', var=var, resultcotation=resultcotation, var_modeda=var_modeda, tipo_moeda=tipo_moeda, unidade=unidade, uf=uf, days_week=days_week, months=months, day_week=day_week, day=day, month=month, year=year, hj=hj, Ass=Ass, tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/fipe_first')
def fipe_first():

  ItensCar.var = Progpy.mark
  varr = ItensCar.var

  var, varx = [],[]
  for a in varr:
    var.append(a[0]) #List car's brand
    varx.append(a[1])
    
  ItensCar.code_car = varx #car brand code


  return render_template('fipe_first.html', var=var)

#Get the car's name
#Here is returned the car's name list
@app.route('/fipe_second', methods = ['POST', 'GET'])
def fipe_second():
  if request.method == 'POST':
    result_fipe2 = request.form

    car_name_brand = result_fipe2['veiculo']
    ItensCar.car_name_brand = car_name_brand

    var = Progpy.name_car(ItensCar.var, ItensCar.car_name_brand)
    ItensCar.id_code = var[-1]

    return render_template('fipe_second.html', var=var, car_name_brand =car_name_brand )

#Get the car's year
#Here is returned the car's year list
@app.route('/fipe_third', methods = ['POST', 'GET'])
def fipe_third():
  if request.method == 'POST':
    result_fipe3 = request.form

    car_name_brand = ItensCar.car_name_brand

    new = result_fipe3['veiculo']
    car_name = new.replace('_', ' ')
    ItensCar.car_name_model = car_name

    var = Progpy.year_car(ItensCar.code_car, ItensCar.car_name_model, ItensCar.id_code)

    return render_template('fipe_third.html', var=var, car_name_brand=car_name_brand, car_name=car_name)

#Result table
#Get the FIPE Tables
@app.route('/fipe_fourth', methods = ['POST', 'GET'])
#@app.route('/fipe_fourth')
def fipe_fourth():
  if request.method == 'POST':
    result_fipe4 = request.form
    print(result_fipe4)
    print('\n\n')

    car_date = result_fipe4['veiculo']

    df = Progpy.final_fipe(ItensCar.car_name_model, ItensCar.id_code, car_date)

    return render_template('fipe_fourth.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
