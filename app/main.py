import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

HOST = "localhost"
PORT = 6379
NUM_THREADS = 5


class RESP:
    @staticmethod
    def resp_single_string(string):
        return f"+{string}\r\n".encode("utf-8")

    @staticmethod
    def null_bulk_string():
        return "$-1\r\n".encode("utf-8")


def calculate_expiration_time(expiry):
    return datetime.now() + timedelta(microseconds=int(expiry) * 1000)


def accept_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while data := conn.recv(1024).decode("utf-8"):
            print("Received: ")
            print(data.replace("\r\n", " "))
            command = data.split("\r\n")[2]
            match command:
                case "echo":
                    word = data.split("\r\n")[-2]
                    conn.send(RESP.resp_single_string(word))
                case "set":
                    if "\r\npx" in data:
                        value, time_delta = data.split("\r\npx")
                        expiry = time_delta.split("\r\n")[-2]
                        key, val = value.split("\r\n")[-4], value.split("\r\n")[-2]
                        memory[key] = {
                            "value": val,
                            "expires": calculate_expiration_time(expiry),
                        }
                    else:
                        key, val = data.split("\r\n")[-4], data.split("\r\n")[-2]
                        memory[key] = {"value": val, "expires": None}
                    conn.send(RESP.resp_single_string("OK"))
                case "get":
                    key = data.split("\r\n")[-2]
                    if key not in memory or (
                        memory[key]["expires"]
                        and datetime.now() > memory[key]["expires"]
                    ):
                        conn.send(RESP.null_bulk_string())
                    else:
                        conn.send(RESP.resp_single_string(memory[key]["value"]))
                case _:
                    conn.send(RESP.resp_single_string("PONG"))


def main():
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        while True:
            conn, addr = server_socket.accept()
            executor.submit(accept_connection, conn, addr)


if __name__ == "__main__":
    memory = {}
    main()
