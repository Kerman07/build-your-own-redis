import socket
from threading import Thread

HOST = "localhost"
PORT = 6379
NUM_THREADS = 2


def accept_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while data := conn.recv(1024):
            print("Received")
            conn.send(b"+PONG\r\n")


def main():
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    server_socket.listen()

    thread_pool = []

    for _ in range(NUM_THREADS):
        conn, addr = server_socket.accept()
        t = Thread(target=accept_connection, args=(conn, addr))
        t.start()
        thread_pool.append(t)

    for thread in thread_pool:
        thread.join()

    server_socket.close()


if __name__ == "__main__":
    main()
