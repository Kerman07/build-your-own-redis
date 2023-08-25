from selectors import DefaultSelector, EVENT_READ
import socket

HOST = "localhost"
PORT = 6379


def accept_connection(server_socket):
    conn, addr = server_socket.accept()
    print("Connected by ", addr)
    conn.setblocking(False)
    selector.register(conn, EVENT_READ)


def handle_client(conn):
    data = conn.recv(1024)
    if data:
        print("Received")
        conn.send(b"+PONG\r\n")
    else:
        print("Connection closed by client")
        selector.unregister(conn)
        conn.close()


def main():
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    server_socket.setblocking(False)

    selector.register(server_socket, EVENT_READ)

    while True:
        events = selector.select()
        for key, _ in events:
            if key.fileobj is server_socket:
                accept_connection(key.fileobj)
            else:
                handle_client(key.fileobj)


if __name__ == "__main__":
    selector = DefaultSelector()
    main()
