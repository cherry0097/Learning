import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 # 0 - 65535 any port you can use. But don't use any already used port
LISTNER_LIMIT = 5
active_clients = [] #All currently connected users

#Function to listen for upcoming messages from client
def listen_for_messages(client,username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_all(message)
        else:
            print(f"The message sent from the client {username} is empty")

#Function to send message to a single client
def send_messages_to_client(client,message):
    client.sendall(message.encode())

#Function to send any new message to all the clients are conneted to the server.
def send_messages_to_all(message):
    for user in active_clients:
        send_messages_to_client(user[1],message)

#Function to handle client
def client_handler(client):
    #Server will listen for client message that will contain the username.
    while 1:
        #recv(): This function is called when we have to listen any messages coming from the specific
        #client. 2048: It's the maximum size limit of the message. decode(): All the messages are sent
        #between client and server are in bytes format. We need to decode them.
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            break
        else:
            print("Client user name is empty")
    
    threading.Thread(target=listen_for_messages, args=(client,username,)).start()


def main():
    #Socket class object 
    #AF_INET: We are going to use IPv4 address
    #SOCK_STREAM: We are going to use TCP protocol.
    #In case we need to use UDP protocol we need to use SOCK_DGRAM
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Creating a try-catch block
    try:
        #Provide the server with an address in the form of host ip and port
        server.bind((HOST,PORT))
        print(f"The server is running on {HOST} {PORT}...")
    except:
        print(f"Unable to bind to host{HOST} and port {PORT}")

    #Set server limit
    server.listen(LISTNER_LIMIT)

    #This while loop will keep listening to client connection
    while 1:
        client, address = server.accept() #This accept funtion will wait for a new connection 
        #and return a new socket representing the connection, and the address of the client. For IP
        #socket the address info is a pair(hostaddr, port)*/
        print(f"Successfully connected to client Host: {address[0]} Port: {address[1]}")

        #Everytime a client is connected a new thread will be created and it will start and
        #that thread will keep running till the time the client is connected to the server.
        threading.Thread(target=client_handler,args=(client,)).start()



if __name__ == '__main__':
    main()