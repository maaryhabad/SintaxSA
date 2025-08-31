class Challenge():
    def __init__(self, name, goal, class_goal, required_attributes, required_methods):
        self.name = name
        self.goal = goal
        self.class_goal = class_goal
        self.required_attributes = required_attributes
        self.required_methods = required_methods

    @staticmethod
    def load_challenges():
        return [Challenge(
            name="Desafio 1: Encapsulamento",
            goal="Crie a classe RobotVacuum com o atributo 'battery' e os métodos 'ligar', 'desligar' e 'aspirar'.",
            class_goal="RobotVacuum",
            required_attributes={'battery'},
            required_methods=["turn_on", "turn_off", "vacuum"])
            # , Challenge(
            # name="Desafio 2: Polimorfismo",
            # goal="Crie a classe SmartLamp (power_on, power_off) e SmartSpeaker (power_on, power_off, play_music).)",
            # class_goal=["SmartLamp", "SmartSpeaker"],
            # )
            ]