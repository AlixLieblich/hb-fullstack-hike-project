import requests

url = "https://community-open-weather-map.p.rapidapi.com/weather"

querystring = {"q":"London,uk","lat":"0","lon":"0","callback":"test","id":"2172797","lang":"null","units":"\"metric\" or \"imperial\"","mode":"xml, html"}
querystring2 = {"lat":"60.18852","lon":"-149.63156"}

headers = {
    'x-rapidapi-key': "8e3f6010abmshc09fe5de80fba0ep138729jsn950d9f17b9e7", #TODO: make it work with WEATHERMAP_KEY
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
response2 = requests.request("GET", url, headers=headers, params=querystring2)

print(response2.text)



