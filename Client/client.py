from pymodbus.client import ModbusTcpClient  # Nowy import

# Ustawienia klienta
SERVER_IP = 'localhost'
PORT = 502

client = ModbusTcpClient(SERVER_IP, port=PORT)

def handle_client_commands():
    client.connect()
    while True:
        command = input("Enter command (status [on/off], speed [value], exit): ")
        if command.startswith("status"):
            _, status = command.split()
            if status.lower() == "on":
                client.write_register(0, 1)  # Włącz turbiny
                print("Turbine turned ON.")
            elif status.lower() == "off":
                client.write_register(0, 0)  # Wyłącz turbiny
                print("Turbine turned OFF.")
            else:
                print("Invalid status. Use 'on' or 'off'.")
        elif command.startswith("speed"):
            _, value = command.split()
            value = int(value)
            client.write_register(1, value)  # Ustawienie docelowej prędkości
            print(f"Target Speed set to {value}.")
        elif command == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid command. Available commands: status [on/off], speed [value], exit.")
    
    client.close()

if __name__ == "__main__":
    handle_client_commands()
