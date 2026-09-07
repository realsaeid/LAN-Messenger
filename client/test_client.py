import socket


SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

username = input("Username: ")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((SERVER_IP, SERVER_PORT))

client.send(username.encode("utf-8"))

response = client.recv(1024).decode("utf-8")

print("Server:", response)

while True:
    message = input("Message: ")

    if message.lower() == "exit":
        break

    client.send(message.encode("utf-8"))

client.close()