import asyncio
from bleak import BleakClient, BleakScanner

# Manufacturer-provided details
padlock_address = "81:2A:75:ED:B4:9F"  # Replace with the actual MAC address or scan to find it
unlock_characteristic_uuid = "0000ffe0-0000-1000-8000-00805f9b34fb"  # Replace with the correct characteristic UUID

UNLOCK_CHARACTERISTIC_UUID = "00002a05-0000-1000-8000-00805f9b34fb"
UNLOCK_COMMAND = bytearray([0xFE, 0x03, 0x01, 0x01, 0x12, 0x34, 0x24])

# Example pairing key
key_string = "zf3uOdDCkmwF2iwGMAsR7if9s08RrFTV"
unlock_command = bytearray(key_string, 'utf-8')

async def scan_and_pair():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device)

    # Replace with the logic to select your padlock
    padlock_device = next((d for d in devices if d.address == padlock_address), None)

    if padlock_device:
        print(f"Found device: {padlock_device}")
        async with BleakClient(padlock_device) as client:
            if await client.is_connected():
                print(f"Connected to {padlock_address}")

                # Example: Attempt pairing (this depends on the BLE device's security level)
                try:
                    await client.pair()
                    print("Pairing successful!")
                except Exception as e:
                    print(f"Pairing failed: {e}")
                    return

                # Send the unlock command
                await client.write_gatt_char(UNLOCK_CHARACTERISTIC_UUID, UNLOCK_COMMAND)
                print("Unlock command sent!")
            else:
                print(f"Failed to connect to {padlock_address}")
    else:
        print("Padlock not found!")

asyncio.run(scan_and_pair())
