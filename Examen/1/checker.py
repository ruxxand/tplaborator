import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


#Partea 1
def build_url(host, path):
    return f"https://{host}{path}"


def is_https(url):
    if url.startswith("https://"):
        return True
    else:
        return False


#Partea 2
def show_response(url):
    r = requests.get(url)
    return f"Status: {r.status_code}, Content-Type: {r.headers.get('Content-Type')}, Length: {len(r.content)}"


#Partea 3
def check_site(url):
    try:
        r = requests.get(url, timeout=5)
        return {
            "status": r.status_code,
            "content_type": r.headers.get("Content-Type"),
            "length": len(r.content),
            "server": r.headers.get("Server", "unknown"),
        }
    except requests.exceptions.RequestException as error:
        return {"status": None, "error": str(error)}


#Partea 4
def scan_sites():
    results = []
    for site in SITES:
        result = check_site(site)
        result["url"] = site
        results.append(result)

    successful = [result for result in results if result["status"] == 200]
    successful.sort(key=lambda result: result.get("length", 0))
    print(f"Reusite: {len(successful)} | Esuate: {len(results) - len(successful)}")
    return successful


#Partea 5
def check_headers(url):
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as error:
        return {"status": None, "error": str(error)}

    response_headers = {header.lower() for header in response.headers}
    present = [
        header
        for header in SECURITY_HEADERS
        if header.lower() in response_headers
    ]
    missing = [
        header
        for header in SECURITY_HEADERS
        if header.lower() not in response_headers
    ]
    score = int(len(present) * 100 / len(SECURITY_HEADERS)) if SECURITY_HEADERS else 0
    return {
        "present": present,
        "missing": missing,
        "score": score,
    }


#Partea 6
def retry_check(url, attempts=3):
    if attempts <= 0:
        return {"status": None, "attempts": 0}

    last_error = None
    last_status = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            if last_status < 500:
                return {"status": last_status, "attempts": attempt}
        except requests.exceptions.RequestException as error:
            last_error = str(error)

    result = {"status": last_status, "attempts": attempts}
    if last_status is None and last_error is not None:
        result["error"] = last_error
    return result
