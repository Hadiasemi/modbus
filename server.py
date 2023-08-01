from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

def run_server():
    # Initialize Data Blocks
    block = ModbusSequentialDataBlock(0x00, [0]*0xff)
    store = ModbusSlaveContext(hr=block, ir=block, co=block, di=block)
    context = ModbusServerContext(slaves=store, single=True)

    # Server Identity
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '1.0'


    try:
        # Run the server
        StartTcpServer(context=context, identity=identity, address=("localhost", 502))
    except:
        pass


if __name__ == "__main__":
    run_server()

