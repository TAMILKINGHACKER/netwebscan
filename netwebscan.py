#!/usr/bin/env python3
import argparse
import socket
import threading
import time
import os
from utils.banner import grab_banner
from utils.output import (
    save_port_results, print_header, print_result, save_summary
)
from subscanner import scan_subdomains, active_subdomains

active_ports = []
inactive_ports = []
lock = threading.Lock()

def scan_target(target, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            banner = ""
            if result == 0:
                banner = grab_banner(s)
                with lock:
                    active_ports.append((port, banner))
                    print_result(port, banner)
            else:
                with lock:
                    inactive_ports.append(port)
    except Exception:
        with lock:
            inactive_ports.append(port)

def scan_ports_on_host(host, ports, timeout, threads, output_prefix):
    global active_ports, inactive_ports
    active_ports = []
    inactive_ports = []

    print_header(host)
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[!] Could not resolve {host}")
        return

    threads_list = []

    for port in ports:
        t = threading.Thread(target=scan_target, args=(ip, port, timeout))
        threads_list.append(t)
        t.start()
        if len(threads_list) >= threads:
            for t in threads_list:
                t.join()
            threads_list = []

    for t in threads_list:
        t.join()

    print(f"[✔] Scan completed for {host}")
    print(f"[✔] Active: {len(active_ports)} | Inactive: {len(inactive_ports)}")

    save_port_results(active_ports, output_prefix + "_active.json")
    save_port_results([(p, "") for p in inactive_ports], output_prefix + "_inactive.json")
    save_summary(output_prefix + "_summary.txt", host, active_ports, inactive_ports)

def start_scan(args):
    ports = range(1, 65536) if args.full_scan else (
        range(int(args.ports.split("-")[0]), int(args.ports.split("-")[1]) + 1)
        if "-" in args.ports else [int(p) for p in args.ports.split(",")]
    )

    print("\n🔍 Starting scan for main target:", args.target)

    try:
        scan_ports_on_host(
            args.target, ports, args.timeout, args.threads, args.output or "result"
        )

        if args.scan_subdomains:
            print("\n🌐 Subdomain Enumeration Enabled")
            scan_subdomains(
                args.target,
                wordlist_file=args.subdomain_wordlist,
                threads=args.threads,
                output_prefix="subdomains"
            )

            for sub, ip in active_subdomains:
                print(f"\n📡 Scanning subdomain: {sub}")
                safe_name = sub.replace(".", "_")
                scan_ports_on_host(
                    sub, ports, args.timeout, args.threads, f"subscan_{safe_name}"
                )

    except KeyboardInterrupt:
        print("\n[⚠] Scan stopped by user. Saving partial results...\n")
        interrupted_prefix = args.output or "interrupted"
        save_port_results(active_ports, f"{interrupted_prefix}_active.json")
        save_port_results([(p, "") for p in inactive_ports], f"{interrupted_prefix}_inactive.json")
        save_summary(f"{interrupted_prefix}_summary.txt", args.target, active_ports, inactive_ports)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NetWebScan v1.6 - Full Port + Subdomain Scanner")
    parser.add_argument("--target", required=True, help="Target IP or domain")
    parser.add_argument("--ports", default="1-1024", help="Ports to scan (e.g. 22,80,443 or 1-1024)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout in seconds")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads")
    parser.add_argument("--output", help="Base name for output files (main target only)")
    parser.add_argument("--full-scan", action="store_true", help="Scan all 65535 TCP ports")
    parser.add_argument("--scan-subdomains", action="store_true", help="Enable subdomain enumeration and scanning")
    parser.add_argument("--subdomain-wordlist", help="Optional subdomain wordlist file")
    args = parser.parse_args()

    start_scan(args)
