from client import TCP_Client
import sys

if __name__ == "__main__":

    if len(sys.argv) != 2:
        port = 10000 # Default port
    else:
        port = int(sys.argv[1])

    client = None
    try:
        client = TCP_Client()
        client.connect("localhost", port)

        isRunning = True
        while isRunning:
            print("Press ctrl+c to disconnect")
            input()

    except KeyboardInterrupt as e:
        if client.isRunning():
            client.disconnect()
    except Exception as e:
        print("exception: " + str(e))