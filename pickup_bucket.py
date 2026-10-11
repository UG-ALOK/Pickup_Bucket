
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PICKUP BUCKET
Website & Network Diagnostics Toolkit
Developer: Firewall-Crusher

Use only on systems you own or are authorized to test.
"""

import os
import sys
import time
import socket
import shutil
import subprocess
import ssl
import ipaddress
import webbrowser
import html
from datetime import datetime
from urllib.parse import urlparse, urljoin

try:
    import requests
except ImportError:
    requests = None


# ==========================================================
# GLOBAL CONFIGURATION
# ==========================================================

APP_NAME = "PICKUP BUCKET"
DEVELOPER = "Firewall-Crusher"

REPORT_DIR = "pickup_bucket_reports"
ROUTE_FILE = "admin_paths.txt"

# Fake Website Request configuration.
# Low-volume diagnostics only; use authorized websites.
FAKE_REQUEST_CONFIG = {
    "DEFAULT_REQUESTS": 9126898,
    "MAX_REQUESTS": 9126898,
    "DELAY_SECONDS": 0,
    "TIMEOUT_SECONDS": 0,
    "METHOD": "GET",  # GET or HEAD
}

DEFAULT_TIMEOUT = 8

# ==========================================================
# ANSI COLOR CODES
# ==========================================================

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

RED = "\033[91m"
DARK_RED = "\033[31m"
WHITE = "\033[97m"
GOLD = "\033[93m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[33m"
BLUE = "\033[94m"

# ==========================================================
# MENU
# ==========================================================

MENU = {
    1: "Website Diagnostics",
    2: "Fake Website Request",
    3: "Admin Panel Finder",
    4: "DNS & Host Lookup",
    5: "HTTP Header Inspector",
    6: "SSL/TLS Certificate Check",
    7: "Redirect Trace",
    8: "Security Header Audit",
    9: "Public & Local IP Overview",
    10: "Local Network Inspector",
    11: "IP Intelligence Lookup",
    12: "Report Center",
}


# ==========================================================
# GENERAL UTILITIES
# ==========================================================

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def setup():
    os.makedirs(REPORT_DIR, exist_ok=True)

    if not os.path.exists(ROUTE_FILE):
        with open(ROUTE_FILE, "w", encoding="utf-8") as file:
            file.write(
                "# Authorized website paths, one per line\n"
                "/admin\n"
                "/login\n"
                "/dashboard\n"
            )


def banner():
    print(f"{RED}{BOLD}")
    print(r"  ____  ___ ____ _  __ _   _ ____")
    print(r" |  _ \|_ _/ ___| |/ /| | | |  _ \ ")
    print(r" | |_) || | |   | ' / | | | | |_) |")
    print(r" |  __/ | | |___| . \ | |_| |  __/")
    print(r" |_|   |___\____|_|\_\ \___/|_|")
    print(RESET)
    print(f"{WHITE}{BOLD}       {APP_NAME}{RESET}")
    print(f"{GOLD}       Developer: {DEVELOPER}{RESET}")
    print(f"{DIM} Website & Network Diagnostics Toolkit{RESET}")
    print(f"{DARK_RED}{'-' * 54}{RESET}")


def pause():
    input(f"\n{GOLD}Press Enter to return to menu...{RESET}")


def require_requests():
    if requests is None:
        print(f"{RED}The requests package is missing.{RESET}")
        print(f"{WHITE}Install: pip install requests{RESET}")
        return False
    return True


def ask_url(prompt="Enter website URL"):
    value = input(f"{WHITE}{prompt}: {RESET}").strip()

    if not value:
        return None

    if "://" not in value:
        value = "https://" + value

    parsed = urlparse(value)

    if (
        parsed.scheme not in ("http", "https")
        or not parsed.hostname
        or parsed.username
        or parsed.password
    ):
        print(f"{RED}Invalid HTTP/HTTPS URL.{RESET}")
        return None

    return value


def make_request(method, url, timeout=DEFAULT_TIMEOUT, **kwargs):
    if not require_requests():
        return None

    try:
        return requests.request(
            method,
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": "PickupBucket/1.0"},
            **kwargs,
        )
    except requests.RequestException as exc:
        print(f"{RED}Request failed: {exc}{RESET}")
        return None


# ==========================================================
# REPORT SYSTEM: TXT + COLORFUL HTML
# ==========================================================

def write_report(title, lines):
    setup()

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(
        char.lower() if char.isalnum() else "_"
        for char in title
    ).strip("_")

    base = f"{safe_title}_{stamp}"
    txt_path = os.path.join(REPORT_DIR, base + ".txt")
    html_path = os.path.join(REPORT_DIR, base + ".html")

    content = "\n".join(str(line) for line in lines)
    generated = datetime.now().isoformat(timespec="seconds")

    with open(txt_path, "w", encoding="utf-8") as file:
        file.write(f"{APP_NAME} - {title}\n")
        file.write(f"Developer: {DEVELOPER}\n")
        file.write(f"Generated: {generated}\n")
        file.write("=" * 60 + "\n")
        file.write(content + "\n")

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
* {{ box-sizing: border-box; }}
body {{
    margin: 0; padding: 22px; background: #080a10;
    color: #f5f6fa; font-family: monospace;
}}
main {{
    max-width: 1000px; margin: auto; overflow: hidden;
    background: #11141c; border: 1px solid #353a48;
    border-radius: 14px;
}}
header {{
    padding: 24px;
    background: linear-gradient(120deg, #600711, #c51e35);
    border-bottom: 3px solid #ffd166;
}}
h1 {{ color: white; }}
.meta {{ color: #ffe2e5; margin-top: 8px; }}
pre {{
    padding: 24px; white-space: pre-wrap;
    overflow-wrap: anywhere; line-height: 1.7;
}}
footer {{
    padding: 16px 24px; color: #ffd166;
    border-top: 1px solid #353a48;
}}
</style>
</head>
<body>
<main>
<header>
<h1>{html.escape(title)}</h1>
<div class="meta">{APP_NAME} | {DEVELOPER}</div>
<div class="meta">{html.escape(generated)}</div>
</header>
<pre>{html.escape(content)}</pre>
<footer>Authorized diagnostics only</footer>
</main>
</body>
</html>"""

    with open(html_path, "w", encoding="utf-8") as file:
        file.write(page)

    print(f"\n{GREEN}Reports saved.{RESET}")
    print(f"{WHITE}TXT: {os.path.abspath(txt_path)}{RESET}")
    print(f"{CYAN}HTML: {os.path.abspath(html_path)}{RESET}")

    return txt_path, html_path


# ==========================================================
# NANO EDITOR
# ==========================================================

def open_in_nano(path):
    editor = shutil.which("nano")

    if not editor:
        print(f"{RED}Nano is not installed.{RESET}")
        print(f"{WHITE}Run: pkg install nano{RESET}")
        print(f"{YELLOW}Manual command: nano {path}{RESET}")
        return False

    try:
        subprocess.run([editor, path], check=False)
        return True
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"{RED}Could not open Nano: {exc}{RESET}")
        print(f"{WHITE}Try manually: nano {path}{RESET}")
        return False


# ==========================================================
# 01 - WEBSITE DIAGNOSTICS
# ==========================================================

def website_diagnostics():
    url = ask_url()
    if not url:
        return

    response = make_request("GET", url)
    if response is None:
        return

    lines = [
        f"URL: {url}",
        f"Final URL: {response.url}",
        f"HTTP status: {response.status_code}",
        f"Response time: {response.elapsed.total_seconds():.3f}s",
        f"Redirects: {len(response.history)}",
        f"Server: {response.headers.get('Server', 'Not disclosed')}",
        f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}",
    ]

    for line in lines:
        print(f"{CYAN}{line}{RESET}")

    write_report("Website Diagnostics", lines)


# ==========================================================
# 02 - FAKE WEBSITE REQUEST
# Configuration is controlled from the top of this file.
# Sequential, low-volume diagnostics for authorized sites.
# ==========================================================

def fake_website_request():
    if not require_requests():
        return

    url = ask_url("Authorized test website URL")
    if not url:
        return

    config = FAKE_REQUEST_CONFIG

    try:
        raw = input(
            f"{WHITE}Request count "
            f"[default {config['DEFAULT_REQUESTS']}]: {RESET}"
        ).strip()

        count = int(raw or config["DEFAULT_REQUESTS"], 10)
    except ValueError:
        print(f"{RED}Enter a valid whole number.{RESET}")
        return

    maximum = int(config["MAX_REQUESTS"])

    if not 1 <= count <= maximum:
        print(f"{RED}Choose between 1 and {maximum}.{RESET}")
        return

    try:
        delay = max(1.0, float(config["DELAY_SECONDS"]))
        timeout = max(1, min(30, int(config["TIMEOUT_SECONDS"])))
    except (ValueError, TypeError):
        print(f"{RED}Invalid request configuration at top of file.{RESET}")
        return

    method = str(config["METHOD"]).upper().strip()

    if method not in ("GET", "HEAD"):
        print(f"{RED}METHOD must be GET or HEAD.{RESET}")
        return

    print(f"\n{GOLD}Fake Request Configuration{RESET}")
    print(f"{WHITE}Method: {method}{RESET}")
    print(f"{WHITE}Request count: {count}/{maximum}{RESET}")
    print(f"{WHITE}Delay: {delay:.1f} seconds{RESET}")
    print(f"{WHITE}Timeout: {timeout} seconds{RESET}")
    print(f"{YELLOW}Use only on a site you own or are authorized to test.{RESET}")

    lines = [
        f"Target: {url}",
        f"Method: {method}",
        f"Request count: {count}",
        f"Delay: {delay} seconds",
        f"Timeout: {timeout} seconds",
    ]

    successful = 0

    for index in range(1, count + 1):
        print(f"{CYAN}[{index:03d}/{count:03d}] Requesting...{RESET}")

        response = make_request(
            method,
            url,
            timeout=timeout,
        )

        if response is None:
            result = f"Request {index}: failed"
            print(f"{RED}{result}{RESET}")
        else:
            elapsed = response.elapsed.total_seconds()
            result = (
                f"Request {index}: HTTP {response.status_code}; "
                f"{elapsed:.3f}s"
            )
            successful += 1
            print(f"{GREEN}{result}{RESET}")

        lines.append(result)

        if index < count:
            time.sleep(delay)

    lines.append(f"Successful requests: {successful}/{count}")
    write_report("Fake Website Request", lines)


# ==========================================================
# 03 - ADMIN PANEL FINDER
# Checks only manually supplied paths; no brute force.
# Nano opens automatically, without a y/N prompt.
# ==========================================================

def admin_panel_finder():
    url = ask_url("Authorized base website URL")
    if not url:
        return

    setup()

    print(f"{GOLD}Opening {ROUTE_FILE} in Nano...{RESET}")
    open_in_nano(ROUTE_FILE)

    try:
        with open(ROUTE_FILE, "r", encoding="utf-8") as file:
            paths = [
                line.strip()
                for line in file
                if line.strip()
                and not line.lstrip().startswith("#")
            ][:100]
    except OSError as exc:
        print(f"{RED}Could not read paths: {exc}{RESET}")
        return

    if not paths:
        print(f"{YELLOW}No paths configured.{RESET}")
        return

    lines = [
        f"Base URL: {url}",
        f"Paths checked: {len(paths)}",
        "Only manually supplied paths were checked.",
    ]

    for index, path in enumerate(paths, 1):
        if not path.startswith("/"):
            path = "/" + path

        target = urljoin(url.rstrip("/") + "/", path.lstrip("/"))
        response = make_request("GET", target)

        if response is None:
            result = f"{target} -> failed"
            print(f"{RED}[{index:02d}] {result}{RESET}")
        else:
            result = f"{target} -> HTTP {response.status_code}"
            print(f"{CYAN}[{index:02d}] {result}{RESET}")

        lines.append(result)

        if index < len(paths):
            time.sleep(0.5)

    write_report("Admin Panel Finder", lines)


# ==========================================================
# 04 - DNS & HOST LOOKUP
# ==========================================================

def dns_host_lookup():
    host = input(f"{WHITE}Hostname: {RESET}").strip()
    if not host:
        return

    lines = [f"Hostname: {host}"]

    try:
        addresses = sorted({
            item[4][0]
            for item in socket.getaddrinfo(host, None)
        })

        for address in addresses:
            print(f"{GREEN}{address}{RESET}")
            lines.append(f"Address: {address}")

    except socket.gaierror as exc:
        print(f"{RED}DNS lookup failed: {exc}{RESET}")
        lines.append(f"DNS lookup failed: {exc}")

    write_report("DNS Host Lookup", lines)


# ==========================================================
# 05 - HTTP HEADER INSPECTOR
# ==========================================================

def http_header_inspector():
    url = ask_url()
    if not url:
        return

    response = make_request("HEAD", url)

    if response is None or response.status_code in (405, 501):
        response = make_request("GET", url, stream=True)

    if response is None:
        return

    lines = [
        f"URL: {response.url}",
        f"HTTP status: {response.status_code}",
        "Headers:",
    ]

    for key, value in response.headers.items():
        line = f"{key}: {value}"
        print(f"{CYAN}{key}:{RESET} {WHITE}{value}{RESET}")
        lines.append(line)

    write_report("HTTP Header Inspector", lines)
    response.close()


# ==========================================================
# 06 - SSL/TLS CERTIFICATE CHECK
# ==========================================================

def ssl_tls_check():
    raw = input(f"{WHITE}Hostname: {RESET}").strip()

    host = urlparse(
        raw if "://" in raw else "https://" + raw
    ).hostname

    if not host:
        print(f"{RED}Invalid hostname.{RESET}")
        return

    lines = [f"Hostname: {host}"]

    try:
        context = ssl.create_default_context()

        with socket.create_connection(
            (host, 443), timeout=DEFAULT_TIMEOUT
        ) as sock:
            with context.wrap_socket(
                sock, server_hostname=host
            ) as secure:
                cert = secure.getpeercert()

                details = [
                    f"TLS version: {secure.version()}",
                    f"Cipher: {secure.cipher()}",
                    f"Issuer: {cert.get('issuer', 'Unknown')}",
                    f"Valid from: {cert.get('notBefore', 'Unknown')}",
                    f"Valid until: {cert.get('notAfter', 'Unknown')}",
                ]

        for line in details:
            print(f"{GREEN}{line}{RESET}")

        lines.extend(details)

    except (OSError, ssl.SSLError, ValueError) as exc:
        print(f"{RED}TLS check failed: {exc}{RESET}")
        lines.append(f"TLS check failed: {exc}")

    write_report("SSL TLS Certificate Check", lines)


# ==========================================================
# 07 - REDIRECT TRACE
# ==========================================================

def redirect_trace():
    url = ask_url()
    if not url:
        return

    response = make_request("GET", url)
    if response is None:
        return

    lines = [f"Start URL: {url}"]

    for index, hop in enumerate(response.history, 1):
        line = (
            f"Hop {index}: HTTP {hop.status_code} "
            f"{hop.url} -> {hop.headers.get('Location', '')}"
        )
        print(f"{GOLD}{line}{RESET}")
        lines.append(line)

    final = f"Final: HTTP {response.status_code} {response.url}"
    print(f"{GREEN}{final}{RESET}")
    lines.append(final)

    write_report("Redirect Trace", lines)


# ==========================================================
# 08 - SECURITY HEADER AUDIT
# ==========================================================

def security_header_audit():
    url = ask_url()
    if not url:
        return

    response = make_request("GET", url)
    if response is None:
        return

    wanted = {
        "Strict-Transport-Security": "HTTPS enforcement",
        "Content-Security-Policy": "Content restrictions",
        "X-Content-Type-Options": "MIME sniffing control",
        "X-Frame-Options": "Frame embedding control",
        "Referrer-Policy": "Referrer privacy",
        "Permissions-Policy": "Browser feature control",
    }

    lines = [f"URL: {response.url}"]

    for header, purpose in wanted.items():
        value = response.headers.get(header)

        if value:
            result = f"PRESENT: {header}: {value}"
            print(f"{GREEN}{result}{RESET}")
        else:
            result = f"MISSING: {header} - {purpose}"
            print(f"{YELLOW}{result}{RESET}")

        lines.append(result)

    write_report("Security Header Audit", lines)


# ==========================================================
# 09 - PUBLIC & LOCAL IP OVERVIEW
# ==========================================================

def public_local_ip_overview():
    lines = [f"Hostname: {socket.gethostname()}"]

    try:
        addresses = sorted({
            item[4][0]
            for item in socket.getaddrinfo(socket.gethostname(), None)
            if ":" not in item[4][0]
            and not item[4][0].startswith("127.")
        })

        local_ip = ", ".join(addresses) if addresses else "Not found"
        lines.append(f"Local IPv4: {local_ip}")

    except OSError as exc:
        lines.append(f"Local IP lookup failed: {exc}")

    if requests is not None:
        try:
            response = requests.get(
                "https://api.ipify.org",
                timeout=DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            lines.append(f"Public IP: {response.text.strip()}")

        except requests.RequestException as exc:
            lines.append(f"Public IP lookup failed: {exc}")
    else:
        lines.append("Install requests to look up public IP.")

    for line in lines:
        print(f"{CYAN}{line}{RESET}")

    write_report("Public Local IP Overview", lines)


# ==========================================================
# 10 - LOCAL NETWORK INSPECTOR
# ==========================================================

def local_network_inspector():
    lines = [
        "Local interface check only.",
        "This option does not scan other devices.",
    ]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.settimeout(2)
        sock.connect(("192.0.2.1", 80))
        result = f"Local interface IPv4: {sock.getsockname()[0]}"

    except OSError as exc:
        result = f"Could not determine local IPv4: {exc}"

    finally:
        sock.close()

    print(f"{CYAN}{result}{RESET}")
    lines.append(result)

    write_report("Local Network Inspector", lines)


# ==========================================================
# 11 - IP INTELLIGENCE LOOKUP
# ==========================================================

def ip_intelligence_lookup():
    raw = input(f"{WHITE}Public IP address: {RESET}").strip()

    try:
        address = ipaddress.ip_address(raw)
    except ValueError:
        print(f"{RED}Invalid IP address.{RESET}")
        return

    if not address.is_global:
        print(f"{YELLOW}Enter a public IP address.{RESET}")
        return

    if not require_requests():
        return

    lines = [f"IP: {address}"]

    try:
        response = requests.get(
            f"https://ipwho.is/{address}",
            timeout=DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("success") is False:
            raise ValueError(data.get("message", "Lookup failed"))

        connection = data.get("connection") or {}

        fields = {
            "Country": data.get("country"),
            "Region": data.get("region"),
            "City": data.get("city"),
            "ISP": connection.get("isp"),
            "Organization": connection.get("org"),
            "ASN": connection.get("asn"),
        }

        for label, value in fields.items():
            if value:
                line = f"{label}: {value}"
                print(f"{CYAN}{line}{RESET}")
                lines.append(line)

        lines.append("Geolocation is approximate.")
        print(f"{YELLOW}IP geolocation is approximate.{RESET}")

    except (requests.RequestException, ValueError) as exc:
        print(f"{RED}Lookup failed: {exc}{RESET}")
        lines.append(f"Lookup failed: {exc}")

    write_report("IP Intelligence Lookup", lines)


# ==========================================================
# 12 - REPORT CENTER
# ==========================================================

def report_center():
    setup()

    files = sorted(
        [
            name for name in os.listdir(REPORT_DIR)
            if name.endswith((".txt", ".html"))
        ],
        reverse=True,
    )

    if not files:
        print(f"{YELLOW}No reports found yet.{RESET}")
        return

    print(f"{GOLD}Report directory: {os.path.abspath(REPORT_DIR)}{RESET}")

    for index, name in enumerate(files, 1):
        print(f"{RED}{index:02d}{RESET}  {CYAN}{name}{RESET}")

    choice = input(
        f"{WHITE}Report number (Enter to return): {RESET}"
    ).strip()

    if not choice:
        return

    try:
        number = int(choice, 10)
        if not 1 <= number <= len(files):
            raise ValueError
    except ValueError:
        print(f"{RED}Invalid report number.{RESET}")
        return

    path = os.path.abspath(
        os.path.join(REPORT_DIR, files[number - 1])
    )

    if files[number - 1].endswith(".html"):
        webbrowser.open("file://" + path)
        print(f"{CYAN}{path}{RESET}")
    else:
        try:
            with open(path, "r", encoding="utf-8") as file:
                print(f"{WHITE}{file.read()}{RESET}")
        except OSError as exc:
            print(f"{RED}Could not read report: {exc}{RESET}")


# ==========================================================
# MAIN MENU
# ==========================================================

def show_menu():
    clear_screen()
    banner()

    for number, label in MENU.items():
        print(f"{RED}{number:02d}{RESET}  {WHITE}{label}{RESET}")

    print(f"{GOLD}00{RESET}  {WHITE}Exit{RESET}")
    print(f"{DARK_RED}{'-' * 54}{RESET}")


def main():
    setup()

    actions = {
        1: website_diagnostics,
        2: fake_website_request,
        3: admin_panel_finder,
        4: dns_host_lookup,
        5: http_header_inspector,
        6: ssl_tls_check,
        7: redirect_trace,
        8: security_header_audit,
        9: public_local_ip_overview,
        10: local_network_inspector,
        11: ip_intelligence_lookup,
        12: report_center,
    }

    while True:
        show_menu()

        choice = input(
            f"{GOLD}Select option (1-12 or 00): {RESET}"
        ).strip()

        if choice in ("0", "00"):
            print(f"{RED}Exiting {APP_NAME}. Goodbye!{RESET}")
            break

        try:
            # Both 3 and 03 are accepted.
            number = int(choice, 10)
        except ValueError:
            print(f"{RED}Enter a valid menu number.{RESET}")
            time.sleep(1)
            continue

        action = actions.get(number)

        if action is None:
            print(f"{RED}Choose an option from 1 to 12.{RESET}")
            time.sleep(1)
            continue

        clear_screen()
        banner()
        print(f"{GOLD}>> {MENU[number]}{RESET}\n")

        try:
            action()
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Operation cancelled.{RESET}")
        except Exception as exc:
            print(f"{RED}Unexpected error: {exc}{RESET}")

        pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}Goodbye.{RESET}")
        sys.exit(0)
