import socket
from _ssl import ssl as _realssl

def patch_ssl(sock, keyfile=None, certfile=None):
    while hasattr(sock, "_sock"):
        sock = sock._sock
    return _realssl(sock, keyfile, certfile)

socket.ssl = patch_ssl
