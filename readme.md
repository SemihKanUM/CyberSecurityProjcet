# Client-Server Counter Project

This project implements a client-server architecture where clients can register, perform actions (increase or decrease a counter), and log out. The server is built using Flask and handles multiple client requests concurrently.

## Project Structure

- **server.py**: The Flask-based server that manages client registration, counter actions (increase/decrease), and logout.
- **client.py**: The client script that reads a configuration file (config.json), registers with the server, performs specified actions, and logs out.
- **config.json**: The client configuration file in JSON format. This file contains client details, server information, and a list of actions for the client to perform.
- **server.log**: A log file that records each action performed by clients, including changes to the counter.

## Requirements

- *Python 3.x*
- *Flask* (pip install flask)
- *Requests* (pip install requests)

## Setup Instructions

1. *Install Dependencies*:
   ```bash
   pip install -r requirements.txt