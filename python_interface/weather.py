import requests
import geocoder

API_KEY = '6fe6249ecc1c082b7317f2c121a311b8'
weather_types = ['Clear', 'Clouds', 'Rain', 'Thunderstorm', 'Drizzle', 'Snow', 'Atmosphere', 'Extreme']
weather_icons = ['sun.png', 'cloud.png', 'rain.png', 'rain.png', 'rain.png', 'snow.png', 'cloud.png', 'extreme.png']

def get_weather():
  location = geocoder.ip('me').latlng
  req = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=imperial'.format(location[0], location[1], API_KEY)
  resp = requests.get(req)

  if resp.status_code != 200:
    raise RuntimeError('Weather API endpoint responded with {}: {}'.format(resp.status_code, resp.json()['message']))

  return resp.json()

def get_icons(weather_data = None):
  if not weather_data:
    weather_data = get_weather()

  # API format
  weather_type = weather_data['weather'][0]['main']
  if weather_type in weather_types:
    icon1 = weather_icons[weather_types.index(weather_type)]
  else:
    icon1 = 'extreme.png'

  temp = int(weather_data['main']['temp'])
  if temp < 0:
    icon2 = ['cold.png']
  elif temp > 99:
    icon2 = ['hot.png']
  else: # temp is a 2 digit number so we can print it
    str_temp = str(temp)
    icon2 = []
    icon2.append('digit_'+str_temp[0]+'.png')
    icon2.append('digit_'+str_temp[1]+'.png')

  return (icon1, icon2)
    

# when run directly just get the weather and print it
if __name__ == '__main__':
  weather = get_weather()
  print(weather)
  print(get_icons(weather))
