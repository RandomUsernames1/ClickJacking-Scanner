from urllib.request import urlopen, Request
from sys import argv, exit
import re

__author__ = 'Aberia_Abelia_Iberia (fixed)'

def check(url):
    """Check if given URL is vulnerable to clickjacking"""

    try:
        if not url.startswith("http"):
            url = "http://" + url

        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urlopen(req, timeout=10)
        headers = dict(data.getheaders())

        # Clickjacking protection headers
        if "x-frame-options" in headers:
            return False
        if "content-security-policy" in headers:
            if "frame-ancestors" in headers["content-security-policy"]:
                return False

        return True

    except Exception as e:
        print(" [!] Error:", e)
        return False


def safe_filename(url):
    """Convert URL into a filesystem-safe filename"""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', url)


def create_poc(url):
    """Create HTML PoC page"""

    filename = safe_filename(url) + ".html"

    code = f"""<!DOCTYPE html>
<html>
<head>
    <title>Clickjacking PoC</title>
</head>
<body>
    <h2>Clickjacking Test</h2>
    <p>If the page below loads inside the iframe, the site is vulnerable and you're a hacker, just like Mr freaking ROBOT!.</p>
    <iframe src="{url}" width="800" height="600"></iframe>
</body>
</html>
"""

    with open(filename, "w") as f:
        f.write(code)

    print(f" [*] PoC saved as: {filename}")


def main():
    try:
        sites = open(argv[1], 'r').read().splitlines()
    except:
        print("[*] Usage: python3 clickjacking_tester.py <sites.txt>")
        exit(0)

    for site in sites:
        print(f"\n[*] Checking {site}")
        vulnerable = check(site)

        if vulnerable:
            print(" [+] Website is vulnerable to clickjacking!")
            create_poc(site)
        else:
            print(" [-] Website is NOT vulnerable")


if __name__ == '__main__':
    main()
