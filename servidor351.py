import socket
import logging

# Configurar el registro de log
logging.basicConfig(
    filename="server_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Servidor escuchando en {host}:{port}")

    while True:
        print("Esperando una conexión...")
        client_socket, client_address = server_socket.accept()
        print(f"Conexión establecida desde {client_address}")

        with client_socket as file_socket:
            file_data = file_socket.recv(1024)
            if file_data:
                with open("received_file.txt", "wb") as received_file:
                    received_file.write(file_data)
                print("Archivo recibido y guardado.")
                logging.info("Archivo recibido y guardado.")


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345

    start_server(HOST, PORT)
