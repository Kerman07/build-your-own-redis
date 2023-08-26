import socket
from concurrent.futures import ThreadPoolExecutor

HOST = "localhost"
PORT = 6379
NUM_THREADS = 5


class RESP:
    @staticmethod
    def resp_single_string(string):
        return bytes(f"+{string}\r\n", "utf-8")


def accept_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while data := conn.recv(1024).decode("utf-8"):
            print("Received: ")
            print(data.replace("\r\n", " "))
            if "\r\necho" in data:
                word = data.split("\r\n")[-2]
                conn.send(RESP.resp_single_string(word))
            else:
                conn.send(RESP.resp_single_string("PONG"))


def main():
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        while True:
            conn, addr = server_socket.accept()
            executor.submit(accept_connection, conn, addr)


if __name__ == "__main__":
    main()
