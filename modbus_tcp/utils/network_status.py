def getIpAdress():
    import socket

    return socket.gethostbyname(socket.gethostname())