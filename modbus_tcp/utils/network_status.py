def get_ip_adress():
    import socket

    return socket.gethostbyname(socket.gethostname())