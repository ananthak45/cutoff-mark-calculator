from flask import Flask, render_template, request
import socket

app = Flask(__name__)

# TCP client function
def send_cutoff_tcp(server_addr, domain, marks):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        print("TCP")
        client_socket.connect(server_addr)
        message = f"{domain},{','.join(marks)}"
        print(f"TCP message sent: {message}")
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        return data.decode()

# UDP client function
def send_cutoff_udp(server_addr, domain, marks):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("UDP")
    message = f"{domain},{','.join(marks)}"
    print(f"UDP message sent: {message}")
    client_socket.sendto(message.encode(), server_addr)
    data, _ = client_socket.recvfrom(1024)
    client_socket.close()
    return data.decode()

# Default route
@app.route('/')
def index():
    return render_template('index.html')

# Route for cutoff calculation
@app.route('/calculate_cutoff', methods=['POST'])
def calculate_cutoff():
    print("Received cutoff calculation request")
    domain = request.form['domain']
    marks = request.form.getlist('marks[]')  # Assuming the names of your input fields are 'marks[]'

    server_ip = '192.168.79.84'  # Replace with your server's IP address
    server_port = 12345           # Replace with your server's port number
    server_addr = (server_ip, server_port)

    # Determine the protocol (You can add a method to get the protocol if needed)
    protocol = 'TCP'  # Change this based on your requirement or input

    # Send data based on the selected protocol
    if protocol == 'TCP':
        response = send_cutoff_tcp(server_addr, domain, marks)
    else:  # protocol == 'UDP'
        response = send_cutoff_udp(server_addr, domain, marks)

    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
