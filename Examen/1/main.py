from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check


def main():
    print("Partea 1:")
    print(build_url("example.com", "/index.html"))
    print(is_https("https://example.com"))
    print(is_https("http://example.com"))

    print("\nPartea 2:")
    print(show_response("https://httpbin.org/status/200"))

    print("\nPartea 3:")
    print(check_site("https://httpbin.org/json"))
    print(check_site("http://this-site-does-not-exist.invalid"))

    print("\nPartea 4:")
    print(scan_sites())

    print("\nPartea 5:")
    print(check_headers(
        "https://httpbin.org/response-headers"
        "?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"
    ))
    print(check_headers("https://httpbin.org/status/200"))

    print("\nPartea 6:")
    print(retry_check("https://httpbin.org/status/200"))
    print(retry_check("https://httpbin.org/status/404"))
    print(retry_check("https://httpbin.org/status/500", attempts=2))
    print(retry_check("http://this-site-does-not-exist.invalid"))


if __name__ == "__main__":
    main()