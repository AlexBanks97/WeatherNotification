import urllib.request, json 

with urllib.request.urlopen("http://vejr.eu/api.php?location=Kastrup&degree=C") as url:
    data = json.loads(url.read().decode())
    print(data)