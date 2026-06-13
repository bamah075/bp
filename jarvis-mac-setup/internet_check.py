import socket


def is_Online():
    """
    Check if the system has an active internet connection
    """
    try:
        # Try to connect to Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except (socket.timeout, socket.error):
        return False
