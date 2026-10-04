# Laborator: funcții, metode și importuri pe web - Partea 3
# Student: Cujbă Ruxanda

import time
import requests
from typing import Optional, Dict, List

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10 

#exercitiu 21
print("\nExercitiu 21")
print("--- Exercițiul 21 ---")

def fetch(url: str):
    """Efectuează o cerere GET către URL și returnează obiectul response."""
    return requests.get(url, timeout=TIMEOUT)

res21 = fetch(BASE_URL)
print("Status code primit de la fetch():", res21.status_code)

#exercitiu 22
print("\nExercitiu 22")
def get_status(url: str) -> int:
    """Returnează doar codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

paths = ["/", "/robots.txt", "/sitemap.xml"]
for p in paths:
    full_url = BASE_URL + p
    status = get_status(full_url)
    print(f"URL: {full_url} -> Status: {status}")
    time.sleep(1)  # Pauză între cereri conform regulilor

#exercitiu 23
print("\nExercitiu 23")
def fetch_with_timeout(url: str, timeout: int = 10):
    """Efectuează o cerere GET având un timp de așteptare implicit (default) de 10 secunde."""
    return requests.get(url, timeout=timeout)

res_default = fetch_with_timeout(BASE_URL)
print("Apel cu timeout implicit - Status:", res_default.status_code)

res_custom = fetch_with_timeout(BASE_URL, timeout=3)
print("Apel cu timeout=3 - Status:", res_custom.status_code)

#exercitiu 24
print("\nExercitiu 24")
def get_title(html: str) -> str:
    """Extrage titlul dintre etichetele <title> și </title> dintr-un cod HTML."""
    start_tag = "<title>"
    end_tag = "</title>"
    
    start = html.find(start_tag)
    if start == -1:
        return "Titlu negăsit"
    
    start += len(start_tag)
    end = html.find(end_tag)
    
    return html[start:end].strip()

# Separare clară: rețeaua e într-o parte, analiza HTML e în funcție
sample_html = res21.text
title = get_title(sample_html)
print("Titlu extras cu get_title():", title)

#exercitiu 25
print("\nExercitiu 25")
help(get_title)


#exercitiu 26
print("\nExercitiu 26")

try:
    get_status(123)
except Exception as e:
    print("Eroare la rulare cand am trimis un numar:", type(e).__name__)

#exercitiu 27
print("\nExercitiu 27")
def page_exists(url: str) -> bool:
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return res.status_code == 200
    except requests.RequestException:
        return False

print("Cybercor există?", page_exists(BASE_URL))
print("Domeniul invalid exista?", page_exists("https://this-domain-does-not-exist.invalid"))


#exercitiu 28
print("\nExercitiu 28")

def check_paths(base: str, paths: List[str]) -> Dict[str, int]:
    results = {}
    for path in paths:
        full_url = base + path
        try:
            res = requests.get(full_url, timeout=TIMEOUT)
            results[path] = res.status_code
        except requests.RequestException:
            results[path] = 0
        time.sleep(1)
    return results
paths_to_check = ["/", "/robots.txt", "/sitemap.xml"]
print("Rezultatele verificării path-urilor:", check_paths(BASE_URL, paths_to_check))

#exercitiu 29
print("\nExercitiu 29")

def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Returnează valoarea unui antet HTTP specificat sau o valoare implicită."""
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return res.headers.get(name, default)
    except requests.RequestException:
        return default

server_header = get_header(BASE_URL, name="Server")
print("Antetul Server este:", server_header)

#exercitiu 30
print("\nExercitiu 30")
def security_headers(url: str) -> Dict[str, bool]:
    target_headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return {h: h in res.headers for h in target_headers}
    except requests.RequestException:
        return {h: False for h in target_headers}

sec_results = security_headers(BASE_URL)
print("Verificare antete securitate:", sec_results)

#exercitiu 31
print("\nExercitiu 31")
def score_headers(results: Dict[str, bool]) -> str:
    present_count = sum(1 for is_present in results.values() if is_present)
    total = len(results)
    return f"{present_count}/{total}"

score = score_headers(security_headers(BASE_URL))
print("Scor securitate antete:", score)

#exercitiu 32
print("\nExercitiu 32")
def fetch_robots(base: str) -> Optional[str]:
    """Returnează conținutul robots.txt sau None dacă fișierul nu există/e eroare."""
    try:
        res = requests.get(base + "/robots.txt", timeout=TIMEOUT)
        if res.status_code == 200:
            return res.text
        return None
    except requests.RequestException:
        return None

def disallowed_paths(robots_text: Optional[str]) -> List[str]:
    if not robots_text:
        return []
    
    disallowed = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.startswith("Disallow:"):
            path = line.split("Disallow:", 1)[1].strip()
            if path:
                disallowed.append(path)
    return disallowed

robots_content = fetch_robots(BASE_URL)
disallowed_list = disallowed_paths(robots_content)
print("Căi interzise în robots.txt:", disallowed_list)

print("Test tratare None:", disallowed_paths(None))

#exercitiu 33
print("\nExercitiu 33")
def response_times(*urls) -> Dict[str, float]:
    times = {}
    for url in urls:
        start = time.perf_counter()
        try:
            requests.get(url, timeout=TIMEOUT)
            elapsed = time.perf_counter() - start
            times[url] = round(elapsed, 4)
        except requests.RequestException:
            times[url] = -1.0
        time.sleep(1)
    return times

r_times = response_times(BASE_URL, ECHO_URL)
print("Timpi de răspuns:", r_times)

#exercitiu 34
print("\nExercitiu 34")
def log(message: str, **details):
    formatted_details = [f"{key}={value}" for key, value in details.items()]
    details_str = " | ".join(formatted_details)
    if details_str:
        print(f"{message} | {details_str}")
    else:
        print(message)

log("verificat", url=BASE_URL, status=200)