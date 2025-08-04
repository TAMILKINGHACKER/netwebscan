import socket
import threading
import os

active_subdomains = []
inactive_subdomains = []
lock = threading.Lock()

def resolve_subdomain(domain, current, total):
    try:
        ip = socket.gethostbyname(domain)
        with lock:
            active_subdomains.append((domain, ip))
            print(f"[✔] ({current}/{total}) {domain} → {ip}")
    except socket.gaierror:
        with lock:
            inactive_subdomains.append(domain)
            print(f"[✘] ({current}/{total}) {domain} → Not Resolved")

def scan_subdomains(base_domain, wordlist_file=None, threads=100, output_prefix="subdomains"):
    global active_subdomains, inactive_subdomains
    active_subdomains = []
    inactive_subdomains = []

    print(f"\n[🔍] Starting Subdomain Enumeration for: {base_domain}\n")

    if wordlist_file:
        try:
            with open(wordlist_file, "r") as f:
                subdomains = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"[!] Wordlist file not found: {wordlist_file}")
            return
    else:
        subdomains = [
            "www", "mail", "ftp", "test", "dev", "portal", "vpn", "admin", "webmail",
            "cpanel", "ns1", "ns2", "blog", "m", "mobile", "cdn", "api", "shop"
        ]

    full_subdomains = [f"{sub}.{base_domain}" for sub in subdomains]
    total = len(full_subdomains)
    threads_list = []

    output_dir = "subdomain_results"
    os.makedirs(output_dir, exist_ok=True)

    for idx, sub in enumerate(full_subdomains):
        t = threading.Thread(target=resolve_subdomain, args=(sub, idx + 1, total))
        threads_list.append(t)
        t.start()

        if len(threads_list) >= threads:
            for t in threads_list:
                t.join()
            threads_list = []

    for t in threads_list:
        t.join()

    # Save results
    active_path = os.path.join(output_dir, f"{output_prefix}_active.txt")
    inactive_path = os.path.join(output_dir, f"{output_prefix}_inactive.txt")

    with open(active_path, "w") as f:
        for d, ip in active_subdomains:
            f.write(f"{d},{ip}\n")

    with open(inactive_path, "w") as f:
        for d in inactive_subdomains:
            f.write(d + "\n")

    print(f"\n[✅] Subdomain Scan Complete!")
    print(f"[✔] Active: {len(active_subdomains)}")
    print(f"[✘] Inactive: {len(inactive_subdomains)}")
    print(f"[📂] Results saved to: {output_dir}/")


# Optional CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Subdomain Enumerator CLI")
    parser.add_argument("--domain", required=True, help="Base domain (e.g. example.com)")
    parser.add_argument("--wordlist", help="Path to wordlist file")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("--output", default="subdomains", help="Output prefix name")

    args = parser.parse_args()

    scan_subdomains(
        args.domain,
        wordlist_file=args.wordlist,
        threads=args.threads,
        output_prefix=args.output
    )
