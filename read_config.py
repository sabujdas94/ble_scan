import asyncio
from bleak import BleakClient

# Replace this with your device's MAC address or UUID
DEVICE_ADDRESS = "81:2A:75:ED:B4:9F"

# The characteristic UUID for writing data (you need to know this for your device)
WRITE_CHAR_UUID = "00001a01-0000-1000-8000-00805f9b34fb"
READ_CHAR_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
# Assembled packet
command = bytearray([0xFE, 0x03, 0x00, 0x00, 0x12, 0x34, 0x22, 0x00])

get_config_command = bytearray([
    0xFE,       # Fixed Byte
    0x03,       # Data Flow (example value, replace if needed)
    0x01, 0x01, # Reserved (not used)
    0x12, 0x34, # Reserved (fill freely, replace if needed)
    0x24,       # Order Code (Get configuration information)
    0x00        # Data Length (no data content)
])
return_config_command = bytearray([
    0xFE,       # Fixed Byte
    0x02,       # Data Flow (example value, replace if needed)
    0x00, 0x00, # Reserved (not used)
    0x12, 0x34, # Reserved (fill freely, replace if needed)
    0x23,       # Order Code (Return configuration information)
    0x00,       # Data Length (4 bytes)
])

async def send_command(address, command):
    async with BleakClient(address) as client:
        await client.write_gatt_char(WRITE_CHAR_UUID, get_config_command)
        print("Command sent")

        # response = await client.read_gatt_char(READ_CHAR_UUID)
        # print("Received response:", response)

        # order_code = response[5]
        # data_length = response[6]
        # data_content = response[7:7 + data_length]
        #
        # print(f"Order Code: 0x{order_code:02X}")
        # print(f"Data Length: {data_length}")
        # print(f"Data Content: {data_content.hex()}")

# Run the command
asyncio.run(send_command(DEVICE_ADDRESS, command))