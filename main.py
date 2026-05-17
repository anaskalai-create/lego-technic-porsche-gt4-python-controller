"""Main application for controlling a LEGO Technic Move Hub with an Xbox controller."""

import asyncio
import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Required by Bleak on Windows when pygame is used in the same application.
if sys.platform == "win32":
    sys.coinit_flags = 0

from util.TechnicMoveHub import TechnicMoveHub
from util.XboxController import XboxController


LIGHTS_ON_ON = 0x00
LIGHTS_ON_BRAKING = 0x01
LIGHTS_OFF_OFF = 0x04
LIGHTS_OFF_BRAKING = 0x05


class Porsche:
    """Coordinates controller input and Bluetooth commands for the LEGO Porsche."""

    def __init__(self):
        self.hub = TechnicMoveHub()
        self.controller = None
        self.lights = LIGHTS_ON_ON
        self.throttle_old = 0
        self.steering_old = 0
        self.lights_old = self.lights
        self.toggle_old = False
        self.was_brake = False

    async def run(self):
        """Start the controller loop."""
        if not await self.hub.scan_and_connect():
            print("Aborting: Verbindung fehlgeschlagen.")
            return

        try:
            self.controller = XboxController()

            if not await self.hub.calibrate_steering():
                print("Aborting: Kalibrierung fehlgeschlagen.")
                return

            while True:
                self.controller.update()

                if self.controller.get_exit():
                    print("Programmende durch Select-Taste.")
                    break

                drive_input = self.controller.get_drive_input()
                reverse_input = self.controller.get_reverse_input()
                steering = self.controller.get_steering()
                brake = self.controller.get_brake()
                throttle = self._determine_throttle(drive_input, reverse_input)

                self._update_lights_toggle()

                if brake and not self.was_brake:
                    self.controller.rumble()
                    lights_mode = self._get_braking_light_mode()
                    await self.hub.drive(0, steering, lights_mode)
                    throttle = 0

                    # Reset the previous throttle value so acceleration works immediately after braking.
                    self.throttle_old = 0

                if not brake and self.was_brake:
                    await self.hub.drive(throttle, steering, self.lights)

                if self._has_changed(throttle, steering) and not brake:
                    print(f"throttle={throttle}, steering={steering}")
                    await self.hub.drive(throttle, steering, self.lights)

                self.was_brake = brake
                self.throttle_old = throttle
                self.steering_old = steering
                self.lights_old = self.lights

                sys.stdout.flush()
                await asyncio.sleep(0.05)

        except KeyboardInterrupt:
            print("Abbruch durch Tastatur.")
        except Exception as error:
            print(f"Unerwarteter Fehler: {error}")
        finally:
            if self.controller:
                self.controller.quit()
            await self.hub.disconnect()

    def _update_lights_toggle(self):
        """Toggle the light state when the configured controller button is pressed."""
        toggle = self.controller.get_toggle_lights()
        if toggle and not self.toggle_old:
            self.lights = LIGHTS_OFF_OFF if self.lights == LIGHTS_ON_ON else LIGHTS_ON_ON
            print("Lichter geändert:", "AN" if self.lights == LIGHTS_ON_ON else "AUS")
        self.toggle_old = toggle

    def _get_braking_light_mode(self):
        """Return the light mode for braking based on the current light state."""
        return LIGHTS_ON_BRAKING if self.lights == LIGHTS_ON_ON else LIGHTS_OFF_BRAKING

    def _has_changed(self, throttle, steering):
        """Check whether a new command needs to be sent to the hub."""
        return (
            steering != self.steering_old
            or throttle != self.throttle_old
            or self.lights != self.lights_old
        )

    @staticmethod
    def _determine_throttle(drive_input, reverse_input):
        """Determine whether the car should drive forward, reverse, or stop."""
        if abs(drive_input) > 3 and abs(reverse_input) <= 3:
            return drive_input
        if abs(reverse_input) > 3 and abs(drive_input) <= 3:
            return reverse_input
        return 0


if __name__ == "__main__":
    asyncio.run(Porsche().run())
