# Modulul webtools.py
# Modul personal cu instrumente pentru analiza site-urilor web
# Student: Ruxanda Cujbă

import time
import json
import socket
import ssl
import hashlib
import re
import urllib.parse
from html.parser import HTMLParser
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple
import requests

# exercitiu 47
print("\nExercitiu 47")
DEFAULT_HEADERS = {"User-Agent": "WebLab-Ruxanda"}
TIMEOUT = 10  


def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)


def get_status(url: str) -> int:
    res = fetch(url)
    return res.status_code


def get_title(html: str) -> str:
    start_tag = "<title>"
    end_tag = "</title>"
    start = html.find(start_tag) + len(start_tag)
    end = html.find(end_tag)
    if start != -1 and end != -1:
        return html[start:end].strip()
    return "Fără titlu"


def security_headers(url: str) -> Dict[str, bool]:
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    results = {}
    try:
        res = fetch(url)
        for h in headers_to_check:
            results[h] = h in res.headers
    except requests.RequestException:
        for h in headers_to_check:
            results[h] = False
    return results


def score_headers(results: Dict[str, bool]) -> str:
    total = len(results)
    passed = sum(1 for present in results.values() if present)
    return f"{passed}/{total}"


def check_paths(base: str, paths: List[str]) -> Dict[str, int]:
    results = {}
    for path in paths:
        full_url = urllib.parse.urljoin(base, path)
        try:
            res = fetch(full_url)
            results[path] = res.status_code
        except requests.RequestException:
            results[path] = 0
        time.sleep(1)
    return results


def extract_links(html: str) -> List[str]:
    raw_links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(raw_links))


def split_links(links: List[str], domain: str) -> Tuple[List[str], List[str]]:
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


def fetch_robots(base: str) -> Optional[str]:
    try:
        url = urllib.parse.urljoin(base, "/robots.txt")
        res = fetch(url)
        if res.status_code == 200:
            return res.text
        return None
    except requests.RequestException:
        return None


def disallowed_paths(robots_text: Optional[str]) -> List[str]:
    if robots_text is None:
        return []
    disallowed = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.startswith("Disallow:"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                path = parts[1].strip()
                if path:
                    disallowed.append(path)
    return disallowed


def resolve(hostname: str) -> str:
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return "IP negăsit"


def cert_days_left(hostname: str) -> int:
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_after_str = cert["notAfter"]
                expire_timestamp = ssl.cert_time_to_seconds(not_after_str)
                now_timestamp = datetime.now(timezone.utc).timestamp()
                seconds_left = expire_timestamp - now_timestamp
                return int(seconds_left // 86400)
    except Exception:
        return 0


# exercitiu 50
print("\nExercitiu 50")
def site_report(url: str) -> Dict:
    parsed_base = urllib.parse.urlparse(url)
    domain = parsed_base.netloc or parsed_base.path

    res = fetch(url)
    status_code = res.status_code
    final_url = res.url

    title = get_title(res.text)

    ip_address = resolve(domain)

    http_url = f"http://{domain}"
    http_res = requests.get(http_url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
    if http_res.history:
        redir_list = [f"{item.status_code} -> {item.url}" for item in http_res.history]
        redirections = " | ".join(redir_list)
    else:
        redirections = "Nicio redirecționare"

    sec_score = score_headers(security_headers(url))

    ssl_days = cert_days_left(domain)

    links = extract_links(res.text)
    internal, external = split_links(links, domain)

    robots_txt = fetch_robots(url)
    forbidden_paths = disallowed_paths(robots_txt)

    report_data = {
        "url": url,
        "status_code": status_code,
        "final_url": final_url,
        "title": title,
        "ip_address": ip_address,
        "redirections": redirections,
        "security_score": sec_score,
        "ssl_cert_days_left": ssl_days,
        "internal_links_count": len(internal),
        "external_links_count": len(external),
        "disallowed_paths": forbidden_paths
    }

    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare:     {status_code}")
    print(f"Titlu:            {title}")
    print(f"Adresă IP:        {ip_address}")
    print(f"Redirecționări:   {redirections}")
    print(f"Scor securitate:  {sec_score}")
    print(f"Certificat:       {ssl_days} de zile rămase")
    print(f"Legături:         {len(internal)} interne, {len(external)} externe")
    print(f"Căi interzise:    {', '.join(forbidden_paths) if forbidden_paths else 'Niciuna'}")

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    print("Salvat în report.json")

    return report_data


# exercitiu 46
print("\nExercitiu 46")
if __name__ == "__main__":
    print("Autotest webtools.py...")
    print("Autotest status cybercor.org:", get_status("https://cybercor.org"))