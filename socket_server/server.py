import socket
from db.connection import DB, UserMessage
import json
from threading import Event

TCP_IP = '0.0.0.0'
TCP_PORT = 5055

db = DB()

def run(ip, port, ready_event: Event):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    ready_event.set()
    print("Socket server is started")

    
    conn, _ = server.accept()

    try:
        with conn:
            while True:
                data = conn.recv(1024)
                parsed_data = json.loads(data.decode())
                db.add_message(UserMessage(
                    username=parsed_data["username"],
                    message=parsed_data["message"]
                ))
                print("All messages: ", db.get_all_messages())
    except KeyboardInterrupt:
        server.close()
    finally:
        server.close()