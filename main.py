import socket, runpy
from colorama import Fore, Back
import threading
import json
"""
This project is client-server application with socket communication.
the client sent commands to the server.
The server research in all the modules of commands it has.
It execute the command if it exists.
Return the result to the client.
"""



def start_server():
    """
    This function simulates a localhost client.
    """

    print(f"{Fore.LIGHTRED_EX}Creating socket...")
    saved_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"{Fore.LIGHTGREEN_EX}Successfully created the socket !")

    port = 101
    print(f"{Fore.LIGHTRED_EX}Binding socket to a port...")
    saved_socket.bind(('', port))
    print(f"{Fore.LIGHTGREEN_EX}Successfully binded the socket !")

    print(f"{Fore.LIGHTRED_EX}Listening to port {port}...")
    saved_socket.listen()
    conn, addr = saved_socket.accept()
    with conn:
        print(f"{Fore.LIGHTRED_EX}Got a link on port {port}.")
        print(f"{Fore.LIGHTYELLOW_EX}Awaiting for data on port {port}.")
        while True:
            data = None
            received_correctly = False
            try:
                data = json.loads(str(conn.recv(2048), 'utf-8'))
                received_correctly = True
            except:
                report_error(conn, "Data is not json or there was an error processing.")
            
            if received_correctly:
                if data:
                    process_data(data, conn, addr)
                    pass
                else:
                    conn.sendall(b"Received empty.")

def process_data(data, conn, addr):
    print(f"{Fore.LIGHTYELLOW_EX}Data received.")
    print(f"{Fore.LIGHTYELLOW_EX}Data is : {data}")
    print(f"{Fore.LIGHTYELLOW_EX}Processing data...")

    if "module_name" not in data.keys() or "function_name" not in data.keys():
        report_error(conn, "Invalid arguments. Correct arguments are : module_name, function_name, parameters.")

    functions_of_path = runpy.run_path(data["module_name"], run_name="__main__")["__all__"]
    result_of_my_function = str(functions_of_path[data["function_name"]](data.get("parameters")))
    conn.sendall(bytes(result_of_my_function, encoding="utf-8"))

def report_error(connection : socket.socket, error : str):
    print(f"{Fore.RED}{error}")
    connection.sendall(bytes(json.dumps({"result":{error}}), encoding="utf-8"))

def send_to_server():
    """
    This function simulates a client that sends a request to the server.
    """

    print(f"{Fore.LIGHTRED_EX}Creating client socket...")
    saved_socket = socket.socket()
    print(f"{Fore.LIGHTGREEN_EX}Successfully created the client socket !\n")
    port = 101
    print(f"{Fore.LIGHTRED_EX}Connect socket to a port...")
    saved_socket.connect(("localhost", port))
    print(f"{Fore.LIGHTGREEN_EX}Successfully binded the socket !\n")
    while True:
        if saved_socket != None:
            
            m = {"module_name" : "sum.py", "function_name" : "sum", "parameters" : (1, 2)} #my parameters
            m2 = "AWAWA !"
            data = json.dumps(m)

            print("It's sending.\n")
            saved_socket.sendall(bytes(data, encoding="utf-8"))
            break
    
    result = None
    while True:
        result = str(saved_socket.recv(2048), 'utf-8')
        if result != None:
            print(f"{Fore.LIGHTCYAN_EX}Data was sent back. The data is {result}.")
            break
    
    while True:
        pass

thread1 = threading.Thread(target=start_server)
thread2 = threading.Thread(target=send_to_server)

thread1.start()
thread2.start()

while True:
    pass