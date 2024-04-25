import socket

#define function to initialize socket connection
def server_start():
    HOST = "127.0.0.1"
    port = 54321

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, port))
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))

    server.listen(5)
    print("Server accepting connections\n")

    client_socket, addr = server.accept()
    print(f"Accepted Connection from client address {addr}")

    while True:
        response = client_socket.recv(1024)
        response = response.decode("utf-8")

        if (response.lower=="close"):
            break
        else:
            print(response)
            data = "Message Received".encode("utf-8")
            client_socket.send(data)


    client_socket.close()
    print(f"Client connection at address {addr} closed")
    server.close()
    print("Server Closed")
    return 0


if __name__ == '__main__':
    server_start()