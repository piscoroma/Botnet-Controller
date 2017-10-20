from server import TCP_Server
import sys
import logging
import datetime

# set log level
log_format = '%(asctime)s %(threadName)s %(filename)s:%(lineno)s %(message)s'
log_date_format = '[%d-%m-%Y %H:%M:%S]'
logging.basicConfig(filename="log_server.log", level=logging.DEBUG, format=log_format, datefmt=log_date_format)


if __name__ == "__main__":

    print("len_argv: " + str(len(sys.argv)))
    if len(sys.argv) != 2:
        port = 10000 # Set default port
    else:
        port = int(sys.argv[1])

    server = None
    try:
        server = TCP_Server(port)
        server.start()

        isRunning = True
        while isRunning:
            print("Choose a command:")
            print("0] Stop server")
            print("1] Show connected clients")
            print("2] Send hello to all clients")
            print("3] Clean old clients")
            print("4] Execute a shell command in all client")
            cmd = input("Choose: ")

            if cmd.isdigit():
                cmd = int(cmd)
                if cmd == 0:
                    print("Stopping server...")
                    server.stop()
                    print("Stopping server...done!")
                    isRunning = False
                elif cmd == 1:
                    print("show all clients")
                    server.show_clients()
                    input()
                elif cmd == 2:
                    print("send hello to all clients")
                    server.hello_all_clients()
                    input()
                elif cmd == 3:
                    print("clean old clients")
                    server.clean_old_clients()
                    input()
                elif cmd == 4:
                    now = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
                    print(now)
                    print("<command> [@hh:mm]")
                    cmd = input("#: ")
                    server.show_clients()
                    print("Write client endpoint to send command, or write all to send to all ")
                    client_endpoint = input("[ip:port] or [all]: ")
                    if client_endpoint.__eq__("all"):
                        server.send_shell_command_to_all_clients(cmd)
                    else:
                        client = server.get_client_by_endpoint(client_endpoint)
                        if client is not None:
                            server.send_shell_command_to_a_client(cmd, client)
                        else:
                            print("client endpoint not valid")
                    input()
                else:
                    print("command not valid")
                    input()
            else:
                print("Error, command not valid")
                input()
    except KeyboardInterrupt as e:
        if server.isRunning():
            print("Stopping server...")
            server.stop()
            print("Stopping server...done!")
    except Exception as e:
        logging.debug("exception: " + str(e))

    print("End")
