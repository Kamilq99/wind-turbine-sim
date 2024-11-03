# Importowanie niezbędnych klas i funkcji z biblioteki pymodbus
from pymodbus.client import ModbusTcpClient  # Klient do komunikacji z serwerem Modbus TCP
import time  # Moduł do operacji związanych z czasem
import random  # Moduł do generowania losowych liczb

# Ustawienia adresu IP i portu serwera SCADA
SERVER_IP = 'localhost'  # Adres IP serwera SCADA
SERVER_PORT = 5020  # Port serwera SCADA

# Funkcja do komunikacji z serwerem SCADA
def run_plc_client():
    client = ModbusTcpClient(SERVER_IP, port=SERVER_PORT)

    if not client.connect():
        print("Failed to connect to SCADA server.")
        return  # Zakończ, jeśli nie można połączyć

    print("Connected to SCADA server.")

    try:
        while True:
            # Odczyt statusu turbiny
            status_response = client.read_holding_registers(0, 1)  # Status turbiny w rejestrze 0
            if not status_response.isError():
                turbine_status = status_response.registers[0]
                print(f"Turbine Status: {'ON' if turbine_status else 'OFF'}")

                if turbine_status == 1:
                    speed_response = client.read_holding_registers(1, 1)  # Odczyt prędkości docelowej
                    if not speed_response.isError():
                        target_speed = speed_response.registers[0]
                        print(f"Target Speed: {target_speed}")

                        # Symulacja zmiany prędkości turbiny
                        new_speed = random.randint(int(target_speed * 0.8), int(target_speed * 1.2))
                        client.write_register(2, new_speed)  # Zapis nowej prędkości do rejestru holding (rejestr 2)
                        print(f"New Speed Sent: {new_speed}")
                else:
                    print("Turbine is OFF. No speed adjustment needed.")
            else:
                print("Failed to read turbine status.")

            time.sleep(1)

    finally:
        client.close()

# Blok główny
if __name__ == "__main__":
    run_plc_client()  # Uruchomienie klienta PLC
