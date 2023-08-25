import socket
from concurrent.futures import ThreadPoolExecutor

HOST = "localhost"
PORT = 6379
NUM_THREADS = 5


def accept_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while data := conn.recv(1024):
            print("Received")
            conn.send(b"+PONG\r\n")


def main():
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    server_socket.listen()

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        while True:
            conn, addr = server_socket.accept()
            executor.submit(accept_connection, conn, addr)


if __name__ == "__main__":
    main()
