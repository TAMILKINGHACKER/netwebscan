import json

def print_header(target):
    print(f"""

    _   __     __ _       __     __   _____                     
   / | / /__  / /| |     / /__  / /_ / ___/_________ _____      
  /  |/ / _ \/ __/ | /| / / _ \/ __ \\__ \/ ___/ __ `/ __ \     
 / /|  /  __/ /_ | |/ |/ /  __/ /_/ /__/ / /__/ /_/ / / / /     
/_/ |_/\___/\__/ |__/|__/\___/_.___/____/\___/\__,_/_/ /_/      
                                                                
          
             NetWebScan - Advanced CLI Scanner
       Advanced Network & Subdomain Enumeration Tool
             Developed by: Krishnamoorthy G
          
---------------------------------------------------------
Target: {target}
""")


def print_result(port, banner):
    print(f"[+] Port {port}/tcp open - {banner}")

def save_port_results(results, filename):
    with open(filename, "w") as f:
        json.dump([{"port": p, "banner": b} for p, b in results], f, indent=2)

def save_summary(filename, target, active, inactive):
    with open(filename, "w") as f:
        f.write(f"Target: {target}\n")
        f.write(f"Total Active Ports: {len(active)}\n")
        f.write(f"Total Inactive Ports: {len(inactive)}\n\n")
        f.write("Active Ports:\n")
        for p, b in active:
            f.write(f" - {p}/tcp: {b}\n")
        f.write("\nInactive Ports:\n")
        for p in inactive:
            f.write(f" - {p}/tcp closed\n")
