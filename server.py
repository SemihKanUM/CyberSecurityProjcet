from flask import Flask, request, jsonify
import threading
import logging

app = Flask(__name__)
clients = {}  # Store client data with counters
lock = threading.Lock()  # Lock to ensure thread safety for concurrent requests

# Set up logging configuration
logging.basicConfig(filename='server.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/register', methods=['POST'])
def register():
    # Extract client data from the request
    data = request.json
    client_id = data.get("id")
    password = data.get("password")

    # Validate that both ID and password are provided
    if not client_id or not password:
        return jsonify({"error": "Missing ID or password"}), 400

    with lock:  # Ensure thread safety
        # Check if the client ID is already registered with a different password
        if client_id in clients and clients[client_id]["password"] != password:
            return jsonify({"error": "ID already registered with a different password"}), 403
        
        # Register the new client if the ID is not already taken
        if client_id not in clients:
            clients[client_id] = {"password": password, "counter": 0}  # Initialize client data
            logging.info(f"Client {client_id} registered successfully.")

    # Respond with success message and initial counter value
    return jsonify({"message": "Registration successful", "counter": clients[client_id]["counter"]}), 201

@app.route('/action', methods=['POST'])
def action():
    # Extract action data from the request
    data = request.json
    client_id = data.get("id")
    password = data.get("password")
    command = data.get("command")
    amount = data.get("amount")

    # Validate that all required fields are provided
    if not client_id or not password or not command or amount is None:
        return jsonify({"error": "Missing required fields"}), 400

    with lock:  # Ensure thread safety
        # Retrieve the client data based on the provided client ID
        client = clients.get(client_id)
        # Validate client credentials
        if not client or client["password"] != password:
            return jsonify({"error": "Unauthorized or client not registered"}), 403

        # Perform the specified action: increase or decrease the counter
        if command == "INCREASE":
            client["counter"] += amount  # Increase counter by the specified amount
        elif command == "DECREASE":
            client["counter"] -= amount  # Decrease counter by the specified amount
        else:
            return jsonify({"error": "Invalid command"}), 400  # Handle invalid commands

        # Log the action with the new counter value
        logging.info(f"{client_id} - {command} {amount}: New counter = {client['counter']}")
        # Respond with success message and updated counter value
        return jsonify({"message": f"{command} successful", "counter": client["counter"]}), 200

@app.route('/logout', methods=['POST'])
def logout():
    # Extract logout data from the request
    data = request.json
    client_id = data.get("id")
    password = data.get("password")

    # Validate that both ID and password are provided
    if not client_id or not password:
        return jsonify({"error": "Missing ID or password"}), 400

    with lock:  # Ensure thread safety
        # Retrieve the client data based on the provided client ID
        client = clients.get(client_id)
        # Validate client credentials
        if not client or client["password"] != password:
            return jsonify({"error": "Unauthorized or client not registered"}), 403

        # Remove client data to simulate logout
        del clients[client_id]  # Erase all data associated with the client
        logging.info(f"Client {client_id} logged out and data removed.")
        # Respond with logout success message
        return jsonify({"message": "Logout successful"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Run the Flask application

