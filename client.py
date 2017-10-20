from exception.network_exception import NetworkException
from network_stream import NetworkStream
from threading import Thread
from utils import Bash
import socket
import logging
import time
import os.path

# set log level
log_format = '%(asctime)s %(threadName)s %(filename)s:%(lineno)s %(message)s'
log_date_format = '[%d-%m-%Y %H:%M:%S]'
logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=log_date_format)

class TCP_Client():

    def __init__(self):
        self.sock = None
        self.networkStream = None
        self.client_is_running = False
        self.server_endpoint = None

    def connect(self, server_ip, server_port):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = (server_ip, server_port)
        self.server_endpoint = str(server_ip) + ':' + str(server_port)
        logging.debug("connecting to " + self.server_endpoint + "...")
        try:
            self.sock.connect(server_address)
            logging.debug("connecting to " + self.server_endpoint + "...done!")
            self.networkStream = NetworkStream(self.sock)
            self.networkStream.send_msg("Hello!")
            logging.debug("Sent: Hello!")
            thread = Thread(target=self._loop_client)
            thread.start()
        except Exception as e:
            logging.debug("Exception: " + str(e))
            self.sock.close()
            logging.debug("Connection closed")
            raise e

    def _loop_client(self):
        self.client_is_running = True
        try:
            while self.isRunning:
                msg = self.networkStream.recv_msg()
                print("[FROM " + self.server_endpoint + "]: " + msg)
                if '#' in msg:
                    cmd = msg.split('#')[1]
                    print("Received command: " + cmd)
                    if '@' in cmd:
                        values = cmd.split('@')
                        cmd = values[0]
                        when = str(values[1])
                        file_log = "cmd_log"
                        file_ack = "ack"
                        file_commands = "commands"
                        cmd_new = cmd + " > " + file_log + " && touch " + file_ack
                        bash = Bash("echo '" + cmd_new + "' > " + file_commands)
                        output = bash.get_output()
                        print(output)
                        bash = Bash("at " + when + " -f " + file_commands)
                        output = bash.get_output()
                        print(output)
                        while not os.path.isfile(file_ack):
                            time.sleep(5)
                        print("Command executed")
                        try:
                            with open(file_log, 'r') as file:
                                data = file.read()
                                file.close()
                                self.networkStream.send_msg(data)
                        except IOError as e:
                            error = "Error during the reading of the file: " + file_log + "\nException: " + str(e)
                            print(error)
                            self.networkStream.send_msg(error)
                        finally:
                            os.remove(file_log)
                            os.remove(file_ack)
                            os.remove(file_commands)
                    else:
                        print("Execute command: " + cmd)
                        bash = Bash(cmd)
                        output = bash.get_output()
                        print(output)
                        self.networkStream.send_msg(output)
                    print("Output sent back to the server")
        except Exception as e:
            if self.client_is_running:
                logging.debug(e)
            self.sock.close()
        logging.debug("Connection closed")


    def isRunning(self):
        return self.client_is_running

    def disconnect(self):
        try:
            self.client_is_running = False
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except self.sock.error as e:
            logging.debug("Error during sock.close, Exception: " + str(e))
            raise NetworkException(e)
