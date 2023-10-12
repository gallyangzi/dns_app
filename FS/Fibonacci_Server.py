from flask import Flask, jsonify, request
import socket

app = Flask(__name__)
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib_list = [0, 1]
        for i in range(2, n):
            fib_list.append(fib_list[i-1] + fib_list[i-2])
        return fib_list

@app.route('/fibonacci/<int:number>')
def get_fibonacci_sequence(number):
    sequence = fibonacci(number)
    return jsonify(sequence=sequence)

@app.route('/register', methods=['POST'])
def register_with_as():
    AS_IP = '127.0.0.1'  
    AS_PORT = 53533  # UDP port of the Authoritative Server

    message = '''TYPE=A
NAME=fibonacci.com
VALUE=127.0.0.1
TTL=10
'''
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            udp_socket.sendto(message.encode(), (AS_IP, AS_PORT))
            data, server = udp_socket.recvfrom(100)
            if data.decode() == "OK":
                return jsonify(status="Successfully registered"), 201
            else:
                return jsonify(status="Failed to register", reason=data.decode()), 500
    except Exception as e:
        return jsonify(status="Error", error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)

