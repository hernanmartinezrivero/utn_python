import socket


def send_file_to_server(host, port, filename):
    with open(filename, "rb") as file:
        file_contents = file.read()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(file_contents)
    client_socket.close()


if __name__ == "__main__":
    HOST = "127.0.0.1"  # Cambia esto a la dirección IP del servidor
    PORT = 12345  # Puerto en el que el servidor está escuchando
    file_to_send = "acciones.txt"

    send_file_to_server(HOST, PORT, file_to_send)
