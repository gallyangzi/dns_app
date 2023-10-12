from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

HOSTNAME_TO_IP = {
    "fibonacci.com": "127.0.0.1"
}

@app.route('/resolve', methods=['GET'])
def resolve_hostname():
    hostname = request.args.get('hostname')
    if not hostname:
        return jsonify(error="Hostname not provided"), 400

    ip_address = HOSTNAME_TO_IP.get(hostname)
    if not ip_address:
        return jsonify(error="Hostname not found"), 404

    return jsonify(ip=ip_address), 200

@app.route('/fibonacci')
def get_fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify({"error": "Missing parameters"}), 400

    try:
        response_as = requests.get(f"http://{as_ip}:{as_port}/resolve?hostname={hostname}")
        if response_as.status_code != 200:
            return jsonify({"error": "Failed to resolve hostname"}), 500
        resolved_ip = response_as.json().get('ip')
        if not resolved_ip:
            return jsonify({"error": "Hostname not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error querying AS: {e}"}), 500

    try:
        response_fs = requests.get(f"http://{resolved_ip}:{fs_port}/fibonacci/{number}")
        if response_fs.status_code != 200:
            return jsonify({"error": "Failed to get Fibonacci number"}), 500
        return response_fs.json(), 200
    except Exception as e:
        return jsonify({"error": f"Error querying FS: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



