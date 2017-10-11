from exception.network_exception import NetworkException
from network_stream import NetworkStream
import time
import logging
import datetime

class ClientHandler():

    def __init__(self, connection, client_address):
        self.conn = connection
        self.client_endpoint = str(client_address[0]) + ':' + str(client_address[1])
        self.client_connected_time = datetime.datetime.now()
        self.networkStream = NetworkStream(self.conn)
        self.clientRunning = False
        self.cmd = None
        self.toRemove = False
        self.file_path = "client_output"

    def start_handler(self):
        try:
            msg = self.networkStream.recv_msg()
            logging.debug("[FROM " + str(self.client_endpoint) + "]: " + msg)
        except NetworkException as e:
            logging.debug("Error during receiving of the message. exception: " + str(e))

        self.clientRunning = True
        while self.clientRunning:
            time.sleep(3)
            if self.cmd is not None:
                if self.cmd.__eq__("hello_message"):
                    try:
                        self.networkStream.send_msg("hello_message")
                    except Exception as e:
                        self.toRemove = True
                        logging.debug(e)
                else:
                    try:
                        self.networkStream.send_msg(self.cmd)
                        data = self.networkStream.recv_msg()
                        # Save the output of the client in a file
                        output_path = None
                        try:
                            output_path = self.file_path + '/' + self.client_endpoint
                            with open(output_path, 'a') as file_output:
                                now = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
                                file_output.write("Received at: " + now + "\n")
                                file_output.write(data + "\n\n")
                            logging.debug("Output from " + str(self.client_endpoint) + " saved in his log file")
                        except Exception as e:
                            logging.debug("Error during the writing of file: " + output_path + "\n" + str(e))
                            print("[FROM " + str(self.client_endpoint) + "]: " + data)
                    except Exception as e:
                        logging.debug(e)
                self.cmd = None

        self.conn.close()
        logging.debug("Connection with " + str(self.client_endpoint) + " closed")

    def stop(self):
        self.clientRunning = False

    def is_to_remove(self):
        return self.toRemove

    def send_command(self, cmd):
        if cmd.__eq__("hello"):
            self.cmd = "hello_message"
        else:
            self.cmd = cmd

    def __str__(self):
        values = self.client_endpoint.split(':')
        string = "{"
        string += "'address': " + values[0] + ", "
        string += "'port': " + values[1] + ", "
        string += "'connected_time': " + self.client_connected_time.strftime("%d/%m/%y %H:%M:%S")
        string += "}"
        return string