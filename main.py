import os
import socket
import threading

user = os.getlogin()
PORT = 37196
console_lock = threading.Lock()

def send_message(ip, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            print(f"Connecting to {ip}...")
            s.connect((ip, PORT))
            print(f"Connected successfully to {ip}!")
            s.sendall(message.encode())
            with console_lock:
                print(f"{user}: {message}")
        except Exception as e:
            with console_lock:
                print(f"Error connecting to {ip}: {e}")

def receive_message():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', PORT))
        s.listen(1)
        print(f"Listening for incoming messages on port {PORT}...")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    message = conn.recv(1024).decode()
                    if message:
                        with console_lock:
                            print(f"{addr}: {message}")
                    else:
                        break

def message_input(ip_to_connect):
    while True:
        message = input(f"{user}: ")
        if message.lower() == 'exit':
            print("Exiting...")
            break
        send_message(ip_to_connect, message)

ip_to_connect = input("ip: ")
print(f"Attempting to connect to {ip_to_connect}...")

receive_thread = threading.Thread(target=receive_message)
receive_thread.daemon = True
receive_thread.start()

message_input(ip_to_connect)
