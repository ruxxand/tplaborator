# Laborator: funcții, metode și importuri pe web
# Student: Cujbă Ruxanda
 

import time
import requests
import urllib.request
from requests import get
import requests as rq

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

# exercitiu 1
print("Exercitiu 1")
print("Versiunea requests:", requests.__version__)

# `urllib` face parte din Biblioteca Standard Python (Standard Library), ceea ce înseamnă că vine 
# preinstalată împreună cu Python. `requests` este o bibliotecă terță (third-party package) creată de 
# comunitate și găzduită pe PyPI (Python Package Index), de aceea necesită instalare separată prin `pip install`.

#exercitiu 2
print("\nExercitiu 2")
# stilul 1
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Răspuns stil 1:", response.status_code)

#stilul 2
response = get(BASE_URL, timeout=TIMEOUT)
print("Răspuns stil 2:", response.status_code)
# Avantaje:
# - Avantaj `import requests`: Claritate și evitarea conflictelor de nume. Este evident în tot codul 
#   că funcția `get` aparține modulului `requests` (evită suprapunerea cu o altă funcție numită `get`).
# - Avantaj `from requests import get`: Concizie. Codul este mai scurt și mai ușor de citit, nefiind 
#   nevoie să repetați numele modulului la fiecare apelare (`get()` în loc de `requests.get()`).

#exercitiu 3
print("\nExercitiu 3")

response_alias = rq.get(BASE_URL, timeout=TIMEOUT)
print("Cod de stare:", response_alias.status_code)
# Când este util / când dăunează un alias:
# - Face codul mai ușor de citit când folosește convenții consacrate în comunitate care scurtează nume lungi
#   (ex: `import pandas as pd`, `import numpy as np`).
# - Face codul mai greu de citit când folosește alias-uri nestandardizate sau obscure (ex: `import requests as rq` sau `import json as j`), 
#   deoarece alți programatori vor trebui să verifice mereu la începutul fișierului ce reprezintă variabila respectivă.

#exercitiu 4
print("\nExercitiu 4")

request_urllib = urllib.request.Request(
    BASE_URL,
    headers={"User-Agent": "Mozilla/5.0 (compatible; WebLab/1.0)"},
)
with urllib.request.urlopen(request_urllib, timeout=TIMEOUT) as response_urllib:
    status = response_urllib.status

    raw_bytes = response_urllib.read(200)
    html_text = raw_bytes.decode("utf-8")

print("Cod de stare (urllib):", status)
print("Primele 200 de caractere:")
print(html_text)

#exercitiu 5
print("\nExercitiu 5")
print(dir(requests))

#Analiza a 3 numere din dir requests:
# 1. `get`: Este o funcție care trimite o cerere HTTP GET
# 2. `Response`: Este o clasă care reprezintă răspunsul primit de la un server după trimiterea unei cereri HTTP.
# 3. `exceptions`: Este un modul care conține clase de excepții specifice pentru gestionarea erorilor în timpul cererilor HTTP.

#exercitiu 6
print("\nExercitiu 6")
# help(requests.get)

# Parametrul care setează timpul maxim de așteptare este `timeout`.
time.sleep(1)
response_timeout = requests.get(BASE_URL, timeout=TIMEOUT)
print("Cerere cu timeout efectuată cu succes. Status:", response_timeout.status_code)

#exercitiu 7
print("\nExercitiu 7")
time.sleep(1)
start_time = time.perf_counter()
res_time = requests.get(BASE_URL, timeout=TIMEOUT)
end_time = time.perf_counter()

total_duration = end_time - start_time
print(f"Timp măsurat cu time.perf_counter(): {total_duration:.4f} secunde")
print(f"Timp raportat de response.elapsed:     {res_time.elapsed.total_seconds():.4f} secunde")

# Comparație:
# `time.perf_counter()` măsoară timpul total "turn-around" din Python (include rezolvarea DNS, crearea 
# conexiunii TCP/SSL, latența de rețea și timpul de procesare internă a obiectului din Python).
# `response.elapsed` măsoară doar timpul scurs între trimiterea antetelor cererii HTTP și primirea antetelor de la server.

#exercitiu 8
print("\nExercitiu 8")
requests.get(BASE_URL, timeout=TIMEOUT)
try:
    import bs4
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")