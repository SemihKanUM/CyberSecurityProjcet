import requests
import json
import time

def load_config(filename):
    """Loads the client configuration from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

def register(client_config):
    """Registers the client with the server."""
    response = requests.post(f"http://{client_config['server']['ip']}:{client_config['server']['port']}/register",
                             json={"id": client_config["id"], "password": client_config["password"]})
    print("Register Response:", response.json())

def perform_actions(client_config):
    """Performs a series of actions (increase or decrease) based on config."""
    delay = client_config["actions"]["delay"]
    for step in client_config["actions"]["steps"]:
        # Split the command and amount from the step string
        command, amount = step.split()
        amount = int(amount)  # Convert amount to integer

        # Send the action request
        response = requests.post(f"http://{client_config['server']['ip']}:{client_config['server']['port']}/action",
                                 json={"id": client_config["id"], "password": client_config["password"],
                                       "command": command, "amount": amount})
        print(f"{command.capitalize()} Response:", response.json())
        
        # Wait for the specified delay before the next action
        time.sleep(delay)


def logout(client_config):
    """Logs the client out from the server, deleting all client data."""
    response = requests.post(f"http://{client_config['server']['ip']}:{client_config['server']['port']}/logout",
                             json={"id": client_config["id"], "password": client_config["password"]})
    print("Logout Response:", response.json())

if __name__ == "__main__":
    # Load the configuration for the client
    config = load_config("config.json")
    
    # Register the client with the server
    register(config)
    
    # Perform actions (INCREASE/DECREASE) as per the configuration
    perform_actions(config)
    
    # Log out the client and clean up server data
    logout(config)
