import requests

BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]


# Partea 1
def search(params):
    r = requests.get(BASE + "/get", params=params)
    return r.json()["args"]


def search_url(params):
    r = requests.get(BASE + "/get", params=params)
    return r.url


# Partea 2
def fetch_with_agent(agent):
    headers = {"User-Agent": agent}
    r = requests.get(BASE + "/headers", headers=headers)
    return r.json()["headers"]["User-Agent"]


def default_agent():
    r = requests.get(BASE + "/headers")
    return r.json()["headers"]["User-Agent"]


# Partea 3
def post_json(data):
    r = requests.post(BASE + "/post", json=data)
    return r.json()["json"]


def post_form(data):
    r = requests.post(BASE + "/post", data=data)
    return r.json()["form"]


# Partea 4
def describe_status(code):
    r = requests.get(f"{BASE}/status/{code}")
    if 200 <= r.status_code < 300:
        return "succes"
    elif 400 <= r.status_code < 500:
        return "eroare client"
    elif 500 <= r.status_code < 600:
        return "eroare server"
    return "necunoscut"


def is_ok(code):
    r = requests.get(f"{BASE}/status/{code}")
    try:
        r.raise_for_status()
        return True
    except requests.HTTPError:
        return False


# Partea 5
def count_redirects(n):
    r = requests.get(f"{BASE}/redirect/{n}")
    return len(r.history)


def final_url(n):
    r = requests.get(f"{BASE}/redirect/{n}")
    return r.url


def first_hop(n):
    r = requests.get(f"{BASE}/redirect/{n}", allow_redirects=False)
    return r.headers.get("Location")


# Partea 6
def cookie_demo(name, value):
    s = requests.Session()
    s.get(f"{BASE}/cookies/set?{name}={value}")
    r = s.get(f"{BASE}/cookies")
    return r.json()["cookies"]


def no_session_demo(name, value):
    """Fă același lucru cu apeluri simple requests.get; returnează cookie-urile văzute de server."""
    requests.get(f"{BASE}/cookies/set?{name}={value}")
    r = requests.get(f"{BASE}/cookies")
    return r.json()["cookies"]


# Partea 7
def report(path):
    url = BASE + path
    try:
        r = requests.get(url, timeout=3)
        content_type = r.headers.get("Content-Type", "").split(";")[0]
        return {
            "status": r.status_code,
            "redirects": len(r.history),
            "final_url": r.url,
            "seconds": round(r.elapsed.total_seconds(), 2),
            "content_type": content_type
        }
    except requests.RequestException as e:
        return {
            "status": None,
            "error": str(e)
        }


def main():
    results = []
    success_count = 0
    fail_count = 0

    for path in PATHS:
        res = report(path)
        res["path"] = path
        results.append(res)
        
        if res.get("status") == 200:
            success_count += 1
        else:
            fail_count += 1

    successful_reports = [r for r in results if r.get("status") == 200]
    successful_reports.sort(key=lambda x: x["seconds"], reverse=True)

    for item in successful_reports:
        print(f"{item['path']} -> {item['status']}, {item['seconds']} secunde")

    print(f"Reușite: {success_count} | Eșuate: {fail_count}")

