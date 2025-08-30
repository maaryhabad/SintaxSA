import unittest
from model.Robot_Vacuum import Robot_Vacuum


class TestRobotVacuum(unittest.TestCase):
    def setUp(self):
        # Cria uma instância do robô com bateria cheia e desligado
        self.robot = Robot_Vacuum(False, (100, 100, 100), 100, 100, 100)

    def test_start_cleaning_only_when_powered_on(self):
        # Não deve começar a andar se estiver desligado
        self.robot.start_cleaning()
        self.assertFalse(self.robot.moving)
        # Liga e tenta novamente
        self.robot.power_on = True
        self.robot.start_cleaning()
        self.assertTrue(self.robot.moving)

    def test_stop_cleaning(self):
        self.robot.power_on = True
        self.robot.start_cleaning()
        self.robot.stop_cleaning()
        self.assertFalse(self.robot.moving)

    def test_update_moves_when_moving(self):
        self.robot.power_on = True
        self.robot.start_cleaning()
        initial_x = self.robot.rect.x
        initial_y = self.robot.rect.y
        self.robot.update()
        self.assertNotEqual(self.robot.rect.x, initial_x)
        self.assertEqual(self.robot.rect.y, initial_y)  # move_direction padrão é (1, 0)

    def test_battery_decreases_when_moving(self):
        self.robot.power_on = True
        self.robot.start_cleaning()
        initial_battery = self.robot.battery_life
        self.robot.update()
        self.assertLess(self.robot.battery_life, initial_battery)

    def test_stops_when_battery_ends(self):
        self.robot.power_on = True
        self.robot.battery_life = 0.01
        self.robot.start_cleaning()
        self.robot.update()
        self.assertFalse(self.robot.moving)
        self.assertEqual(self.robot.battery_life, 0)