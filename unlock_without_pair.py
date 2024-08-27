import asyncio
from bleak import BleakClient

# Replace these with your device's MAC address and UUIDs
DEVICE_MAC_ADDRESS = "81:2A:75:ED:B4:9F"
# UNLOCK_CHARACTERISTIC_UUID = "0000ffd2-0000-1000-8000-00805f9b34fb"
UNLOCK_CHARACTERISTIC_UUID = "00002a05-0000-1000-8000-00805f9b34fb"

MODEL_NBR_UUID = 0x24

# Print the formatted byte array
# UNLOCK_COMMAND = bytearray([0x7a, 0x66, 0x33, 0x75, 0x4f, 0x64, 0x44, 0x43, 0x6b, 0x6d, 0x77, 0x46, 0x32, 0x69, 0x77, 0x47, 0x4d, 0x41, 0x73, 0x52, 0x37, 0x69, 0x66, 0x39, 0x73, 0x30, 0x38, 0x52, 0x72, 0x46, 0x54, 0x56])

UNLOCK_COMMAND = bytearray([0xFE, 0x03, 0x01, 0x01, 0x12, 0x34, 0x24])
async def unlock_padlock(address):
    async with BleakClient(address) as client:
        # Write the unlock command to the characteristic
        await client.write_gatt_char(UNLOCK_CHARACTERISTIC_UUID, UNLOCK_COMMAND)
        print("Padlock unlocked!")

if __name__ == "__main__":
    asyncio.run(unlock_padlock(DEVICE_MAC_ADDRESS))
