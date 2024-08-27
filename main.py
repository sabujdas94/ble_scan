import asyncio
from bleak import BleakClient, BleakScanner
import hashlib
import uuid

# Define the target device name and address (address will be determined during scanning)
TARGET_ADDRESS = "81:2A:75:ED:B4:9F"
# UUIDs and Key as strings
service_uuid = "jx01b2449134b6c4"

uuid_hex_string = "jx01b2449134b6c4"

key_hex_string = "zf3uOdDCkmwF2iwGMAsR7if9s08RrFTV"

# Convert to bytearray
unlock_command = bytearray(key_hex_string.encode('utf-8'))


def string_to_uuid(input_string):
    # Hash the string using SHA-1 and take the first 128 bits (32 characters)
    hash_object = hashlib.sha1(input_string.encode('utf-8')).hexdigest()[:32]

    # Format it as a UUID
    formatted_uuid = f"{hash_object[:8]}-{hash_object[8:12]}-{hash_object[12:16]}-{hash_object[16:20]}-{hash_object[20:32]}"

    return str(uuid.UUID(formatted_uuid))

async def unlock_padlock():
    async with BleakClient(TARGET_ADDRESS) as client:
        # Check if the padlock is connected
        if await client.is_connected():
            print(f"Connected to {TARGET_ADDRESS}")

            unlock_characteristic_uuid = string_to_uuid(uuid_hex_string)

            print("Unlock Characteristic UUID:", unlock_characteristic_uuid)

            # Send the unlock command
            await client.write_gatt_char(unlock_characteristic_uuid, unlock_command)
            print("Unlock command sent!")

        else:
            print(f"Failed to connect to {TARGET_ADDRESS}")

async def connect_and_discover(address):
    try:
        print(address)
        async with BleakClient(address) as client:
            print(f"Connected to {address}")

            #
            # model_number = await client.read_gatt_char(MODEL_NBR_UUID)
            # print("Model Number: {0}".format("".join(map(chr, model_number))))
            #
            # # Check if the device is connected
            # if client.is_connected:
            #     print(client)
            #     # print(f"Device Name: {client.name.strip()}")  # Trim leading and trailing spaces
            #
            #     # Discover services and characteristics
            #     services = await client.get_services()
            #     for service in services:
            #         print(f"Service: {service.uuid}")
            #         for characteristic in service.characteristics:
            #             print(f"  Characteristic: {characteristic.uuid}")
            #
            #             # Optionally read the characteristic value
            #             try:
            #                 value = await client.read_gatt_char(characteristic.uuid)
            #                 print(f"    Value: {value}")
            #             except Exception as e:
            #                 print(f"    Error reading characteristic {characteristic.uuid}: {e}")

    except Exception as e:
        print(f"Error connecting to {address}: {e}")


async def run_scanner():
    global target_address

    def detection_callback(device, advertisement_data):
        global target_address
        # Trim and compare device name
        address = device.address.strip() if device.name else ""
        if address == TARGET_ADDRESS:
            print(f"Target Device Found! Name: {address}, Address: {device.address}")
            target_address = device.address
            # Stop scanning
            asyncio.create_task(stop_scanning())

    async def stop_scanning():
        # Stop scanning after device is found
        await scanner.stop()
        print("Scanning stopped.")
        # Now that scanning is stopped, try to connect to the device
        if target_address:
            await connect_and_discover(target_address)

    # Create a BleakScanner instance with the detection_callback
    global scanner
    scanner = BleakScanner(detection_callback=detection_callback)
    print("Scanning for devices...")
    await scanner.start()

    # Run the scanner for a specified duration (it will stop early if the target device is found)
    await asyncio.sleep(2000)  # Scan for up to 10 seconds


# Run the scanner in the asyncio event loop
async def main():
    await run_scanner()


asyncio.run(unlock_padlock())
