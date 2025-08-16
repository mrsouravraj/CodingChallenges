#!/usr/bin/env python3
import socket
import sys
import re

def whois_query(query: str, server: str, port: int = 43) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server, port))
        sock.sendall((query + "\r\n").encode("utf-8"))
        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
    return response.decode("utf-8", errors="replace")

def parse_whois_response(response: str) -> dict:
    result = {}
    for line in response.splitlines():
        line = line.strip()
        if not line or line.startswith("%") or line.startswith("#"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            if key in result:
                if isinstance(result[key], list):
                    result[key].append(value)
                else:
                    result[key] = [result[key], value]
            else:
                result[key] = value
    return result

def get_referred_server(parsed: dict) -> str | None:
    if "whois" in parsed:
        return parsed["whois"]
    if "refer" in parsed:
        return parsed["refer"]
    return None

def is_ip_address(query: str) -> bool:
    ipv4_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    ipv6_pattern = r"^[0-9a-fA-F:]+$"
    return re.match(ipv4_pattern, query) or re.match(ipv6_pattern, query)

def whois_recursive(query: str, start_server: str = "whois.iana.org"):
    server = start_server
    visited = set()
    while server and server not in visited:
        visited.add(server)
        print(f"\n=== Querying {server} ===")
        try:
            raw = whois_query(query, server)
        except Exception as e:
            print(f"Error querying {server}: {e}")
            break
        print(raw)
        parsed = parse_whois_response(raw)
        server = get_referred_server(parsed)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <domain_or_ip>")
        sys.exit(1)
    domain = sys.argv[1]
    whois_recursive(domain)

if __name__ == "__main__":
    main()