import socket
import ssl
def server_start():
    HOST = "127.0.0.1"
    port = 54321
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='selfsigned.crt', keyfile='private.key')
    
    context.check_hostname = False

    # Create and bind the socket
    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, port))
        print("Socket successfully created and is listening")
        server.listen(5)
    except socket.error as err:
        print("Socket creation failed with error %s" % err)
        server.close()
        return

    while True:
        print("Server accepting connections")
        try:
            client_socket, addr = server.accept()
            print(f"Accepted connection from client address {addr}")

            # Wrap the client socket in SSL
            secure_server = context.wrap_socket(client_socket, server_side=True)
            handle_client(secure_server, addr)
        except ssl.SSLError as e:
            print(f"SSL error occurred: {e}")
        except Exception as e:
            print(f"Error handling connection from {addr}: {e}")
        finally:
            client_socket.close()



    
#def function that checks for the user credential (no hash yet)
def check_credentials(username, password):
    with open("credentials.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(',')
            if stored_username == username and stored_password == password:
                return True 
    return False

def handle_client(secure_server, addr):

    try:
        secure_server.send("Insert Username:".encode("utf-8"))
        username = secure_server.recv(1024).decode("utf-8")
        secure_server.send("Insert Password:".encode("utf-8"))
        password = secure_server.recv(1024).decode("utf-8")
        
        if check_credentials(username, password):
            print("Client connected")
            secure_server.send("Login successful".encode("utf-8"))
            manage_session(secure_server, addr)
        else:
            secure_server.send("Login failure".encode("utf-8"))
            print(f"Login failed, client connection at address {addr} closed")
    except Exception as e:
        print(f"Error during client communication: {e}")
        
def manage_session(secure_server, addr):

    try:
        while True:
            message = secure_server.recv(1024).decode("utf-8")
            if message.lower() == "close":
                print(f"Client connection at address {addr} closed")
                break
            else:
                print(f"Received from {addr}: {message}")
                secure_server.send("Message Received".encode("utf-8"))
    except Exception as e:
        print(f"Session management error with {addr}: {e}")
    finally:
        secure_server.close()
if __name__ == '__main__':
    server_start()