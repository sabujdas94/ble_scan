import asyncio
from bleak import BleakClient, BleakScanner

# Define the target device name and address (address will be determined during scanning)
TARGET_ADDRESS = "81:2A:75:ED:B4:9F"

# Store the address of the target device once found
target_address = None


async def connect_and_discover(address):
    try:
        print(address)
        async with BleakClient(address) as client:
            print(f"Connected to {address}")

            # Check if the device is connected
            if client.is_connected:
                print(client)
                # print(f"Device Name: {client.name.strip()}")  # Trim leading and trailing spaces

                # Discover services and characteristics
                services = await client.get_services()
                for service in services:
                    print(f"Service: {service.uuid}")
                    for characteristic in service.characteristics:
                        print(f"  Characteristic: {characteristic.uuid}")

                        # Optionally read the characteristic value
                        try:
                            value = await client.read_gatt_char(characteristic.uuid)
                            print(f"    Value: {value}")
                        except Exception as e:
                            print(f"    Error reading characteristic {characteristic.uuid}: {e}")

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


asyncio.run(main())
