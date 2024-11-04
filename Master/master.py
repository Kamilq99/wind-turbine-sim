# master.py
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
from threading import Thread
import random
import time

# Konfiguracja rejestrów SCADA
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*10),
    co=ModbusSequentialDataBlock(0, [0]*10),
    hr=ModbusSequentialDataBlock(0, [0]*10),
    ir=ModbusSequentialDataBlock(0, [0]*10)
)

context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = 'SCADA System'
identity.ProductCode = 'TurbineControl'
identity.ProductName = 'Wind Turbine SCADA'
identity.ModelName = 'SCADA Simulator'
identity.MajorMinorRevision = '1.0'

def update_turbine():
    while True:
        # Odczyt statusu turbiny i docelowej prędkości z rejestrów
        status = store.getValues(3, 0, count=1)[0]  # Status turbiny (0 = OFF, 1 = ON)
        target_speed = store.getValues(3, 1, count=1)[0] if status == 1 else 0

        # Symulacja prędkości i produkcji energii, jeśli turbina jest włączona
        if status == 1:
            current_speed = random.randint(int(target_speed * 0.8), int(target_speed * 1.2))
            current_energy = current_speed * 5
        else:
            current_speed = 0
            current_energy = 0

        # Zapis aktualnej prędkości i energii do rejestrów
        store.setValues(4, 0, [current_speed])  # Rejestr 4, adres 0: aktualna prędkość
        store.setValues(4, 1, [current_energy])  # Rejestr 4, adres 1: energia

        print(f"Turbine Status: {'ON' if status else 'OFF'}, Target Speed: {target_speed}, Current Speed: {current_speed}, Energy: {current_energy}")
        time.sleep(1)

def run_server():
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 502))

if __name__ == "__main__":
    server_thread = Thread(target=run_server)
    server_thread.start()
    update_thread = Thread(target=update_turbine)
    update_thread.start()
