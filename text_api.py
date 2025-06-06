import requests

API_KEY = "8a1be0ec-3083-11f0-b77d-0242ac130003-8a1be146-3083-11f0-b77d-0242ac130003"
CITY = "Douala"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

resp = requests.get(URL)
print(resp.status_code, resp.text)
