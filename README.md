NetWebScan

Advanced Network & Subdomain Scanner (CLI Tool)

NetWebScan is a powerful command-line Python tool that performs:

Full TCP port scanning (active & inactive ports)

Subdomain enumeration (active & inactive subdomains)

Banner grabbing on open ports

Real-time threaded scanning with optional wordlist support

Developed by: Krishnamoorthy G Cybersecurity Student – Dhanalakshmi Srinivasan College of Engineering and Technology

🔧 Features

Full port scan (1–65535 TCP ports)

Detects both open and closed ports

Subdomain enumeration with built-in or custom wordlist

Banner grabbing support for services

Graceful shutdown (Ctrl+C saves partial results)

Real-time progress and results printing

Threaded for fast scanning

Output results saved to files: JSON, TXT

📁 Project Structure

netwebscan/
├── netwebscan.py               # Main CLI scanner script
├── subscanner.py               # Subdomain enumeration module
├── utils/
│   ├── __init__.py
│   ├── banner.py               # Banner grabbing logic
│   └── output.py               # Print/save helpers
├── wordlists/
│   └── top-subdomains.txt      # (Optional) Wordlist
├── results/                    # Output folder (auto-created)
├── requirements.txt            # Dependencies
└── README.md                   # This file

🚀 Installation

1. Clone the repository

git clone https://github.com/your-username/netwebscan.git
cd netwebscan

2. Install requirements

pip install -r requirements.txt

🧪 Usage

🔍 Basic full port scan

python netwebscan.py --target scanme.nmap.org --full-scan

🎯 Scan specific port range

python netwebscan.py --target scanme.nmap.org --ports 20-100

🌐 Subdomain enumeration

python netwebscan.py --target example.com --scan-subdomains

📂 Use custom subdomain wordlist

python netwebscan.py --target example.com \
    --scan-subdomains --subdomain-wordlist wordlists/top-subdomains.txt

💾 Save output to files

python netwebscan.py --target example.com --output results/scan1

🆘 Show Help Command

python netwebscan.py --help

Displays all available command-line options and usage examples.

📦 Output Files

scan1_active.json – list of open ports with banners

scan1_inactive.json – list of closed ports

scan1_summary.txt – summary report

subdomain_results/subdomains_active.txt – resolved subdomains with IPs

subdomain_results/subdomains_inactive.txt – unresolvable subdomains

subscan_subdomain_com_active.json – scan results per subdomain

🛠 Requirements

Python 3.6+

Only 1 external library:

colorama>=0.4.6

Install with:

pip install -r requirements.txt

⚠️ Disclaimer

This tool is developed for educational and authorized security testing purposes only. Do not use it on targets without permission.

👨‍💻 Author

Krishnamoorthy GB.E. Cyber SecurityDhanalakshmi Srinivasan College of Engineering and Technology

GitHub: your-username

📜 License

MIT License (optional)

🌟 Credits

ASCII art by pyfiglet

Built-in tools: socket, threading, argparse, os, etc.

Happy scanning, da Macha! 🕵️‍♂️💻

