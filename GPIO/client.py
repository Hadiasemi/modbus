from pymodbus.client import ModbusTcpClient
import time


client = ModbusTcpClient('10.11.14.69', port=5020)
client.connect()

try:
    while True:
        client.write_coil(20, 1)
        print(client.read_coils(20, 1).bits[0])
        time.sleep(1)
        client.write_coil(20, 0)
        print(client.read_coils(20, 1).bits[0])
        time.sleep(1)
except KeyboardInterrupt:
    client.write_coil(20, 0)
    print("exit")

