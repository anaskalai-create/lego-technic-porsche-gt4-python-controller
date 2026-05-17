"""Bluetooth communication for the LEGO Technic Move Hub."""

from bleak import BleakClient, BleakScanner


class TechnicMoveHub:
    """Handles BLE scanning, pairing and motor commands for the LEGO Technic Move Hub."""

    def __init__(self, device_name="Technic Move"):
        self.device_name = device_name
        self.characteristic_uuid = "00001624-1212-EFDE-1623-785FEABCD123"
        self.client = None
        self.is_paired = False

    async def scan_and_connect(self) -> bool:
        """Scan for the hub, connect to it and pair the device."""
        print("Scanning for devices...")
        devices = await BleakScanner.discover(timeout=10.0)

        for device in devices:
            if device.name and self.device_name in device.name:
                print(f"Found device: {device.name} - {device.address}")
                self.client = BleakClient(device)

                try:
                    await self.client.connect()
                except Exception as error:
                    print(f"Connection failed: {error}")
                    return False

                if self.client.is_connected:
                    print(f"Connected to {device.name}")
                    try:
                        paired = await self.client.pair(protection_level=2)
                    except Exception as error:
                        print(f"Pairing failed: {error}")
                        return False

                    if paired:
                        print(f"Paired with {device.name}")
                        self.is_paired = True
                        return True

        print("Connection or pairing failed.")
        return False

    async def send_data(self, data) -> bool:
        """Send raw bytes to the hub via BLE."""
        if not self.client or not self.client.is_connected or not self.is_paired:
            print("Client not connected or paired.")
            return False

        try:
            await self.client.write_gatt_char(self.characteristic_uuid, data)
            return True
        except Exception as error:
            print(f"Write failed: {error}")
            return False

    async def calibrate_steering(self) -> bool:
        """Send the steering calibration sequence to the hub."""
        if self.client and self.client.is_connected and self.is_paired:
            await self.send_data(bytes.fromhex("0d008136115100030000001000"))
            await self.send_data(bytes.fromhex("0d008136115100030000000800"))
            return True
        return False

    async def drive(self, speed=0, steering=0, lights=0):
        """Send motor, steering and light values to the hub."""
        data = bytearray([
            0x0D, 0x00, 0x81, 0x36, 0x11, 0x51,
            0x00, 0x03, 0x00, speed & 0xFF, steering & 0xFF, lights, 0x00,
        ])
        return await self.send_data(data)

    async def disconnect(self):
        """Disconnect from the BLE device if a connection exists."""
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            print("Disconnected from LEGO Technic Move Hub.")
