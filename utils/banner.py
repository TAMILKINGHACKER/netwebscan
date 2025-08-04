def grab_banner(sock):
    try:
        sock.settimeout(1)
        banner = sock.recv(1024).decode().strip()
        return banner if banner else "Unknown"
    except:
        return "Unknown"
