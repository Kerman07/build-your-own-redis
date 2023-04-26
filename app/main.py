import socket

HOST = "localhost"
PORT = 6379


def main():
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    conn, addr = server_socket.accept()  # wait for client
    with conn:
        print(f"Connected by {addr}")
        while data := conn.recv(1024):
            conn.send(b"+PONG\r\n")


if __name__ == "__main__":
    main()
