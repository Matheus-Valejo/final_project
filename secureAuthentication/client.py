import socket

def client_start():

    HOST = "127.0.0.1"
    port = 54321

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, port))
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))

    while True:
        data = input("Enter message  -  ('Close' to close connection):  ")
        client.send(data.encode("utf-8")[:1024])

        if (data.lower() == "close"):
            break
        else:
            response = client.recv(1024)
            response = response.decode("utf-8")
            print(response)


    # close client socket (connection to the server)
    client.close()
    print("Connection to server closed")

    return 0

if __name__ == '__main__':
    client_start()