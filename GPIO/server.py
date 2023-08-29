import asyncio
import logging
from gpiozero import LED
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import StartAsyncTcpServer


logging.basicConfig()
_logger = logging.getLogger(__file__)
_logger.setLevel(logging.INFO)
_logger.disabled = False

led = LED(21)

class CallbackDataBlock(ModbusSequentialDataBlock):
    """A datablock that stores the new value in memory,

    and passes the operation to a message queue for further processing.
    """

    def __init__(self, queue, addr, values):
        """Initialize."""
        self.queue = queue
        super().__init__(addr, values)

    def setValues(self, address, value):
        """Set the requested values of the datastore."""
        if address == 21:
            if value[0] == 0:
                led.on()
                print("LED ON")
            else:
                led.off()
                print("LED OFF")
        super().setValues(address, value)
        
        txt = f"Callback from setValues with address {address}, value {value}"
        _logger.debug(txt)

    def getValues(self, address, count=1):
        """Return the requested values from the datastore."""
        result = super().getValues(address, count=count)
        txt = f"Callback from getValues with address {address}, count {count}, data {result}"
        _logger.debug(txt)
        return result

    def validate(self, address, count=1):
        """Check to see if the request is in range."""
        result = super().validate(address, count=count)
        txt = f"Callback from validate with address {address}, count {count}, data {result}"
        _logger.debug(txt)
        return result


async def run_async_server():
    """Run server."""
    txt = f"### start ASYNC server, listening on 5020 - localhost"
    _logger.info(txt)
    identity = ModbusDeviceIdentification(
        info_name={
            "VendorName": "Pymodbus",
            "ProductCode": "PM",
            "VendorUrl": "https://github.com/pymodbus-dev/pymodbus/",
            "ProductName": "Pymodbus Server",
            "ModelName": "Pymodbus Server",
            "MajorMinorRevision": '',
        }
    )
   
    queue = asyncio.Queue()
    block = CallbackDataBlock(queue, 0x00, [0] * 100)
    #block.setValues(1, 15)
    store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    context = ModbusServerContext(slaves=store, single=True)
    server = await StartAsyncTcpServer(
        context=context,  # Data storage
        identity=identity,  # server identify
        address=('', 5020),  # listen address
    )
    


if __name__ == "__main__":
    asyncio.run(run_async_server(), debug=False)  # pragma: no cover
