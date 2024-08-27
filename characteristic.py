from bleak import BleakClient


async def get_unlock_characteristic_uuid(address):
    async with BleakClient(address) as client:
        services = await client.get_services()

        # Iterate through services and characteristics
        for service in services:
            for char in service.characteristics:
                # Print UUIDs of characteristics
                print(f"Service UUID: {service.uuid}")
                print(f"Characteristic UUID: {char.uuid}")

                # Check for unlock characteristic UUID if you know it
                # For example, if you know the unlock characteristic UUID is '0000abcd-0000-1000-8000-00805f9b34fb'
                if char.uuid == '0000abcd-0000-1000-8000-00805f9b34fb':
                    print(f"Unlock Characteristic UUID: {char.uuid}")
                    return char.uuid

        print("Unlock characteristic not found")
        return None


# Use the function
import asyncio

TARGET_ADDRESS = "81:2A:75:ED:B4:9F"
asyncio.run(get_unlock_characteristic_uuid(TARGET_ADDRESS))
