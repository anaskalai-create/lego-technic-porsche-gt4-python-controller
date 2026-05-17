"""Xbox controller input handling using pygame."""

import pygame


class XboxController:
    """Reads throttle, steering, brake, light and exit input from an Xbox controller."""

    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            raise RuntimeError("Kein Joystick gefunden.")

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print(f"Joystick erkannt: {self.joystick.get_name()}")

    def update(self):
        """Refresh pygame controller events."""
        pygame.event.pump()

    def quit(self):
        """Stop pygame and release controller resources."""
        pygame.quit()

    def get_drive_input(self):
        """Return forward throttle value from 0 to 100."""
        return round(((self.joystick.get_axis(5) + 1) / 2) * 100)

    def get_reverse_input(self):
        """Return reverse throttle value from 0 to -100."""
        return -round(((self.joystick.get_axis(4) + 1) / 2) * 100)

    def get_steering(self):
        """Return steering value from -80 to 80 with a small dead zone."""
        value = round(self.joystick.get_axis(0) * 80)
        return value if abs(value) >= 5 else 0

    def get_brake(self):
        """Return True while the brake button is pressed."""
        return self.joystick.get_button(5)

    def get_toggle_lights(self):
        """Return True while the light toggle button is pressed."""
        return self.joystick.get_button(0)

    def get_exit(self):
        """Return True while the exit button is pressed."""
        return self.joystick.get_button(6)

    def rumble(self):
        """Trigger a short controller rumble feedback."""
        self.joystick.rumble(0.0, 0.3, 300)
