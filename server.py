import socket
import logging
import time
from threading import Thread
import threading
from client_handler import ClientHandler

class TCP_Server():

    def __init__(self, port):
        self.address = "0.0.0.0"
        self.port = port
        self.sock = None
        self.server_is_running = None
        self.clients = None
        self.lock = threading.Lock()

    def start(self):
        self.server_is_running = True
        thread = Thread(target=self._loop_clients)
        thread.start()

    def _loop_clients(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = (self.address, self.port)
        logging.debug("Server started on " + self.address + ":" + str(self.port))
        self.sock.bind(server_address)

        # Listen for incoming connections
        self.sock.listen(1)

        self.clients = []
        while self.server_is_running:
            logging.debug("Waiting for a connection...")
            connection = None
            try:
                connection, client_address = self.sock.accept()
                if self.server_is_running:
                    logging.debug("connection accepted from " + str(client_address))
                    client = ClientHandler(connection, client_address)
                    thread = Thread(target=client.start_handler)
                    thread.start()
                    self.lock.acquire()
                    self.clients.append(client)
                    self.lock.release()
            except Exception as e:
                logging.debug("Server forced to stop")
                if connection is not None:
                    connection.close()

    def stop(self):
        logging.debug("Server stopping...")
        self.server_is_running = False
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        logging.debug("There are " + str(len(self.clients)) + " clients to stop")
        for client in self.clients:
            client.stop()
        logging.debug("Server stopping...done!")

    def isRunning(self):
        return self.server_is_running

    def hello_all_clients(self):
        if len(self.clients) > 0:
            for client in self.clients:
                client.send_command("hello")
        else:
            print("No clients connected")

    def clean_old_clients(self):
        logging.debug("Start cleaner...")
        clients_to_remove = 0
        self.lock.acquire()
        try:
            new_clients = []
            for client in self.clients:
                client.send_command("hello")
            time.sleep(1)
            for client in self.clients:
                if client.is_to_remove():
                    logging.debug("Client " + str(client.client_endpoint) + " has to be removed")
                    clients_to_remove = clients_to_remove + 1
                    client.stop()
                else:
                    new_clients.append(client)
            self.clients = new_clients
        except Exception as e:
            logging.debug("Start cleaner...Error: " + str(e))
        finally:
            self.lock.release()
        logging.debug("Start cleaner...Finished! Removed: " + str(clients_to_remove) + " old clients")

    def get_client_by_endpoint(self, client_endpoint):
        for client in self.clients:
            if client.client_endpoint.__eq__(client_endpoint):
                return client
        return None

    def send_shell_command_to_a_client(self, cmd, client):
            client.send_command("shell#"+cmd)
            logging.debug("Command sent to client: " + client.client_endpoint)

    def send_shell_command_to_all_clients(self, cmd):
        if len(self.clients) > 0:
            for client in self.clients:
                client.send_command("shell#"+cmd)
            logging.debug("Command sent to all clients: " + cmd)
        else:
            print("No clients connected")

    def show_clients(self):
        self.lock.acquire()
        if len(self.clients) > 0:
            for client in self.clients:
                print(client.__str__())
        else:
            print("No clients connected")
        self.lock.release()
