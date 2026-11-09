from socket_server.server import run as run_socket, TCP_IP, TCP_PORT
from http_server.server import run as run_http
import threading


if __name__ == "__main__":
    # TCP Server
    tcp_thread = threading.Thread(
        target=run_socket,
        args=(TCP_IP, TCP_PORT),
        daemon=True
    )

    # HTTP Server
    http_thread = threading.Thread(
        target=run_http,
        daemon=True
    )

    tcp_thread.start()
    http_thread.start()

    tcp_thread.join()
    http_thread.join()