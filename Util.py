import socket


def getIpInfo():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.168.0.1', 1))
        ipAddress = s.getsockname()[0]
        return 'IP: ' + ipAddress;
        # TODO auch prüfen, ob erreichbar, sonst ausgeben, dass nicht erreichbar
    except Exception:
        return 'Netzwerk ???'
        # Fehlermeldung verarbeiten
    finally:
        s.close()
