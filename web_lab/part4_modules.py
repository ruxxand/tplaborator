# Laborator: funcții, metode și importuri pe web - Partea 4
# Student: Ruxanda Cujbă

import time
import json
import socket
import ssl
import hashlib
import re
from datetime import datetime, timezone
import urllib.parse
from html.parser import HTMLParser
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  

#exercitiu 35
print("\nExercitiu 35")

def parse_url_demo(url_str: str):
    parsed = urllib.parse.urlparse(url_str)
    print("Scheme (protocol):", parsed.scheme)
    print("Netloc (domeniu):  ", parsed.netloc)
    print("Path (cale):       ", parsed.path)
    print("Query (parametri): ", parsed.query)
    print("Fragment (ancoră): ", parsed.fragment)

parse_url_demo("https://cybercor.org/path?x=1#top")

#exercitiu 36
print("\nExercitiu 36")
def build_absolute_urls(base: str, relative_paths: list) -> list:
    return [urllib.parse.urljoin(base, path) for path in relative_paths]

relative_links = ["/about", "contact.html", "../index.html"]
absolute_links = build_absolute_urls(BASE_URL, relative_links)

for rel, abs_url in zip(relative_links, absolute_links):
    print(f"Cale relativă: {rel:<15} -> URL absolut: {abs_url}")


#exercitiu 37
print("\nExercitiu 37")

def extract_links(html: str) -> list:
    raw_links = re.findall(r'href="([^"]+)"', html)
    unique_links = list(dict.fromkeys(raw_links))
    return unique_links

res_37 = requests.get(BASE_URL, timeout=TIMEOUT)
found_links = extract_links(res_37.text)
print(f"S-au găsit {len(found_links)} legături unice. Primele 5:")
for link in found_links[:5]:
    print(" -", link)

#exercitiu 38
print("\nExercitiu 38")

def split_links(links: list, domain: str) -> tuple:
    internal = []
    external = []
    
    for link in links:
        full_url = urllib.parse.urljoin(f"https://{domain}", link)
        netloc = urllib.parse.urlparse(full_url).netloc
        
        if netloc == domain or netloc.endswith("." + domain):
            internal.append(full_url)
        else:
            external.append(full_url)
            
    return internal, external

internal_links, external_links = split_links(found_links, "cybercor.org")
print(f"Legături interne: {len(internal_links)} | Legături externe: {len(external_links)}")

#exercitiu 39
print("\nExercitiu 39") 

class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            attrs_dict = dict(attrs)
            src_val = attrs_dict.get("src") or attrs_dict.get("SRC")
            if src_val:
                self.images.append(src_val)
                
test_html = """
<html><body>
<img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)
print("Imagini găsite în testul local:", finder.images)

assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp",
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul pe HTML-ul cunoscut A TRECUT cu succes!")

real_finder = ImageFinder()
real_finder.feed(res_37.text)
print(f"Site-ul real cybercor.org are {len(real_finder.images)} imagini găsite prin tag <img>.")
for img_src in real_finder.images:
    print(" -", img_src)
    
#exercitiu 40
print("\nExercitiu 40")

def page_fingerprint(url: str) -> str:
    res = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(res.content).hexdigest()

hash1 = page_fingerprint(BASE_URL)
hash2 = page_fingerprint(BASE_URL)

print("Amprenta 1:", hash1)
print("Amprenta 2:", hash2)
print("Sunt ambele amprente identice?", hash1 == hash2)

#exercitiu 41
print("\nExercitiu 41")
with open("headers.json", "w", encoding="utf-8") as f:
    json.dump(dict(res_37.headers), f, indent=2)
print("Antetele au fost salvate în 'headers.json'.")

with open("headers.json", "r", encoding="utf-8") as f:
    loaded_headers = json.load(f)

print("Antetul Content-Type citit din fișierul JSON:", loaded_headers.get("Content-Type"))


#exercitiu 42
print("\nExercitiu 42")

def resolve(hostname: str) -> str:
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return "IP negăsit"

ip_cybercor = resolve("cybercor.org")
print("Adresa IP pentru cybercor.org este:", ip_cybercor)


#exercitiu 43
print("\nExercitiu 43")

def cert_days_left(hostname: str) -> int:
    context = ssl.create_default_context()
    
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            
            not_after_str = cert["notAfter"]
            expire_timestamp = ssl.cert_time_to_seconds(not_after_str)
            
            now_timestamp = datetime.now(timezone.utc).timestamp()
            seconds_left = expire_timestamp - now_timestamp
            
            days = int(seconds_left // 86400)
            return days

days_remaining = cert_days_left("cybercor.org")
print(f"Certificatul SSL pentru cybercor.org mai este valabil {days_remaining} zile.")