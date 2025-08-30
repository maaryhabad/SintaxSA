import unittest

import pygame
from model.Smart_Lamp import Smart_Lamp

class TestSmartLamp(unittest.TestCase):
    def setUp(self):
        self.lamp = Smart_Lamp(100, 100)

    def test_initial_state(self):
        self.assertFalse(self.lamp.power_on)
        self.assertEqual(self.lamp.color, (255, 255, 0))

    def test_power_on(self):
        self.lamp.power_on = False
        self.lamp.power_on = True
        self.assertTrue(self.lamp.power_on)

    def test_power_off(self):
        self.lamp.power_on = True
        self.lamp.power_off()
        self.assertFalse(self.lamp.power_on)

    def test_draw_runs(self):
        # Testa se o método draw pode ser chamado sem erro
        screen = pygame.Surface((200, 200))
        try:
            self.lamp.draw(screen)
        except Exception as e:
            self.fail(f"draw() raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()