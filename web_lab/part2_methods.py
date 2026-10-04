# Laborator: funcții, metode și importuri pe web - Partea 2
# Student: Cujbă Ruxanda

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  


# ecercitiu 9
print("\nExercitiu 9")
response = requests.get(BASE_URL, timeout=TIMEOUT)

print("status_code:", response.status_code) #Atribut
print("ok:", response.ok) #Atribut
print("url:", response.url) #Atribut
print("encoding:", response.encoding) #Atribut

#exercitiu 10
print("\nExercitiu 10")
response.raise_for_status()
invalid_url = ECHO_URL + "/status/404"

try:
    bad_response = requests.get(invalid_url, timeout=TIMEOUT)
    bad_response.raise_for_status()
except requests.HTTPError as error:
    print(f"Eroare HTTP prinsa cu succes! Pagina nu a fost gasita: {error}")

time.sleep(1)

#exercitiu 11
print("\nExercitiu 11")
for name, value in response.headers.items():
    print(f"{name}: {value}")

#exercitiu 12
print("\nExercitiu 12")
server = response.headers.get("Server", "lipsește")
content_type = response.headers.get("Content-Type", "lipsește")
content_type_lower = response.headers.get("content-type", "lipsește")

print("Server: ", server)
print("Content-Type: ", content_type)
print("content-type: ", content_type_lower)

#exercitiu 13
print("\nExercitiu 13")
cyber_count = response.text.lower().count("cyber")
print("Cuvantul 'cyber' apare de: ", cyber_count, ' ori')

#ecercitiu 14
print("\nExercitiu 14")
html = response.text
start_tag = "<title>"
end_tag = "</title>"

start = html.find(start_tag) + len(start_tag)
end = html.find(end_tag)

raw_title = html[start:end]
clean_title = raw_title.strip()

print("Titlul paginii:", clean_title)

#exercitiu 15
print("\nExercitiu 15")

lines = html.splitlines()
print("Numar total de linii: ", len(lines))

if lines:
    longest_line = max(lines, key=len)
    print("Cea mai lungă linie are", len(longest_line), "caractere.")

#exercitiu 16
print("\nExercitiu 16")
if response.url.startswith("https://"):
    print("Conexiune securizta")
else:
    print("Conexiune nesecurizata")

#exercitiu 17
print("\nExercitiu 17")

redirect_response = requests.get(BASE_URL, timeout=TIMEOUT)

print("Istoric redirecționări:")
for item in redirect_response.history:
    print(f" -> [{item.status_code}] {item.url}")

print("URL final după redirecționări:", redirect_response.url)
time.sleep(1)

#exercitiu 18
print("\nExercitiu 18")
head_res = requests.head(BASE_URL, timeout=TIMEOUT)
get_res = requests.get(BASE_URL, timeout=TIMEOUT)

print("Lungimea corpului HEAD: ", len(head_res.content))
print("Lungimea corpului GET: ", len(get_res.content))

#exercitiu 19
print("\nExercitiu 19")

cookies = response.cookies

if len(cookies) == 0:
    print("Nici un cookie selectat")
else:
    for cookie in cookies: 
        print(f"Cookie: {cookie.name} | Secure: {cookie.secure}")


#exercitiu 20
print("\nExercitiu 20")
session = requests.Session()
session.headers.update({"User-Agent": "Ruxanda"})

echo_response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
headers_received = echo_response.json().get("headers", {})

print("Antetul User-Agent primit de server:", headers_received.get("User-Agent"))