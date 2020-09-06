from flask import Flask,render_template,request
import requests

app = Flask(__name__)

class Weather():
    def __init__(self,city):
        self.url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=API_LEY'.format(city)

    def get_weather(self):
        data = dict()
        try:
            response = requests.get(self.url).json()
            data['temp'] = str(round(response['main']['temp']-273.15))
            data['min_temp'] = str(round(response['main']['temp_min']-273.15))
            data['max_temp'] = str(round(response['main']['temp_max']-273.15))
            data['city'] = response['name']
            data['desc'] = response['weather'][0]['description']
            data['code'] = 200
            return data
        except:
            data['code']=404
            return data

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city')
        w = Weather(city)
        data=w.get_weather()
        if(data['code']==200):
            return render_template('index.html',data=data,error=None)
        else:
            return render_template('index.html',error="City not Found!",data="")
       
    else:
        w = Weather("Bangalore")
        data=w.get_weather()
        return render_template('index.html',data=data)

    


if __name__ == '__main__':
    app.run()
