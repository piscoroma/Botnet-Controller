from exception.network_exception import NetworkException
import socket
import struct
import logging

class NetworkStream():

    def __init__(self, socket):
        self.sock = socket

    def send_msg(self, msg):
        try:
            # Prefix each message with a 4-byte length (network byte order)
            msg = struct.pack('>I', len(msg)) + msg.encode('utf-8')
            self.sock.sendall(msg)
        except Exception as e:
            raise NetworkException(e)

    def recv_msg(self):
        try:
            # Read message length and unpack it into an integer
            raw_msglen = self._recvall(4)
            msglen = struct.unpack('>I', raw_msglen)[0]
            # Read the message data
            data = self._recvall(msglen)
            data = data.decode('utf-8')
            return data
        except RuntimeError as e:
            logging.debug("socket connection broken")
            raise NetworkException(e)
        except Exception as e:
            raise NetworkException(e)

    def _recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        try:
            packet = None
            bytes_received = 0
            while bytes_received < n:
                chunk = self.sock.recv(n - bytes_received)
                if chunk == '':
                    raise RuntimeError("socket connection broken")
                if packet is None:
                    packet = chunk
                else:
                    packet = packet + chunk
                bytes_received = bytes_received + len(chunk)
            return packet
        except Exception as e:
            #logging.debug("_recvall exception: " + str(e))
            raise e
