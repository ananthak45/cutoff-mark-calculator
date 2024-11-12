import socket

def calculate_cutoff(domain, marks):
    if domain == "engineering":
        return (2 * int(marks[0]) + 4 * int(marks[1]) + 2 * int(marks[2])) / 8
    elif domain == "medical":
        return (2 * int(marks[0]) + 4 * int(marks[1]) + 2 * int(marks[2])) / 8
    elif domain == "commerce":
        return sum(int(m) / 4 for m in marks)
    elif domain == "law":
        return sum(int(m) / 4 for m in marks)
    elif domain == "mba":
        return (int(marks[0]) / 2 + int(marks[1]) / 4 + int(marks[2]) / 4)
    elif domain == "msc":
        return (int(marks[0]) / 2 + int(marks[1]) / 2)
    else:
        return 0

def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("TCP server listening on port 12345")
    
    while True:
        conn, addr = server.accept()
        print(f"Connected by tcp {addr}")
        data = conn.recv(1024).decode()
        domain, *marks = data.split(',')
        result = calculate_cutoff(domain, marks)
        conn.sendall(f"{result}".encode())
        conn.close()

def udp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('0.0.0.0', 12345))
    print("UDP server listening on port 12345")
    
    while True:
        data, addr = server.recvfrom(1024)
        print(f"Connected by udp {addr}")
        domain, *marks = data.decode().split(',')
        result = calculate_cutoff(domain, marks)
        server.sendto(f"{result}".encode(), addr)

if __name__ == "__main__":
    from threading import Thread

    Thread(target=tcp_server).start()
    Thread(target=udp_server).start()
