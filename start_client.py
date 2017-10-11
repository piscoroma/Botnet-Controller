from client import TCP_Client
import sys
import time

if __name__ == "__main__":

    if len(sys.argv) != 2:
        remote_address = "localhost"
        remote_port = 10000 # Default port
    else:
        remote_endpoint = sys.argv[1]
        remote_address = remote_endpoint.split(':')[0]
        remote_port = int(remote_endpoint.split(':')[1])

    client = None
    try:
        client = TCP_Client()

        imConnected = False
        count = 1
        while not imConnected:
            try:
                client.connect(remote_address, remote_port)
                imConnected = True
            except Exception as e:
                print("Failed connection attempt..." + str(count))
                count += 1
                time.sleep(1)

        isRunning = True
        while isRunning:
            print("Press ctrl+c to disconnect")
            input()

    except KeyboardInterrupt as e:
        if client.isRunning():
            client.disconnect()
    except Exception as e:
        print("Exited")