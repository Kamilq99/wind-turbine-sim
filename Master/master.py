# Importowanie niezbędnych klas i funkcji z biblioteki pymodbus
from pymodbus.server import StartTcpServer      # Funkcja do uruchomienia serwera Modbus TCP
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext  # Kontekst dla serwera Modbus
from pymodbus.datastore import ModbusSequentialDataBlock  # Blok danych do przechowywania rejestrów
from pymodbus.device import ModbusDeviceIdentification  # Klasa do identyfikacji urządzenia
from threading import Thread  # Klasa do uruchamiania wątków
import random  # Moduł do generowania losowych liczb
import time    # Moduł do operacji związanych z czasem

# Konfiguracja rejestrów SCADA
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*10),  # 10 dyskretnych wejść (di)
    co=ModbusSequentialDataBlock(0, [0]*10),  # 10 wyjść (co)
    hr=ModbusSequentialDataBlock(0, [0]*10),  # 10 rejestrów holding (hr)
    ir=ModbusSequentialDataBlock(0, [0]*10)   # 10 rejestrów wejściowych (ir)
)

# Tworzenie kontekstu serwera Modbus z utworzonymi rejestrami
context = ModbusServerContext(slaves=store, single=True)

# Ustawienia identyfikacji urządzenia
identity = ModbusDeviceIdentification()
identity.VendorName = 'SCADA System'
identity.ProductCode = 'TurbineControl'
identity.ProductName = 'Wind Turbine SCADA'
identity.ModelName = 'SCADA Simulator'
identity.MajorMinorRevision = '1.0'

# Funkcja aktualizująca dane turbiny
def update_turbine():
    # **Zmienianie statusu turbiny i prędkości docelowej**
    # Włącz turbiny i ustaw docelową prędkość
    store.setValues(3, 0, [1])  # Ustawienie statusu turbiny na ON (1)
    store.setValues(3, 1, [1500])  # Ustawienie prędkości docelowej na 1500 (możesz zmienić tę wartość)
    while True:
        # Sprawdzenie statusu turbiny
        status = store.getValues(3, 0, count=1)[0]  # Odczyt statusu z rejestru hr
        target_speed = store.getValues(3, 1, count=1)[0] if status == 1 else 0  # Odczyt prędkości docelowej

        # Symulacja bieżącej prędkości i poziomu energii
        current_speed = random.randint(int(target_speed * 0.8), int(target_speed * 1.2)) if status == 1 else 0
        current_energy = current_speed * 5

        # Aktualizacja rejestrów
        store.setValues(4, 0, [current_speed])  # Ustawienie aktualnej prędkości
        store.setValues(4, 1, [current_energy]) # Ustawienie aktualnego poziomu energii

        # Wyświetlenie statusu turbiny
        print(f"Turbine Status: {'ON' if status else 'OFF'}, Target Speed: {target_speed}, Current Speed: {current_speed}, Energy: {current_energy}")

        time.sleep(1)

# Funkcja do uruchomienia serwera Modbus
def run_server():
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 5020))  # Używamy adresu 0.0.0.0

# Blok główny
if __name__ == "__main__":
    server_thread = Thread(target=run_server)
    server_thread.start()
    update_thread = Thread(target=update_turbine)
    update_thread.start()
