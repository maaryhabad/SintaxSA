class GameController:
    def __init__(self, current_challenge, feedback_message, class_in_progress, defined_classes, input_box_active, input_name_class, instantiated_objects, intro):
        self.current_challenge = current_challenge
        self.feedback_message = feedback_message
        self.class_in_progress = class_in_progress
        self.defined_classes = defined_classes
        self.input_box_active = input_box_active
        self.input_name_class = input_name_class
        self.instantiated_objects = instantiated_objects
        self.intro = intro

    @staticmethod
    def start_challenge(self):
        GameController(
            current_challenge=1,
            feedback_message="Bem vindo ao Laboratório",
            class_in_progress= {'nome': '', 'attributes': set(), 'methods': set()},
            defined_classes={},
            input_box_active=False,
            input_name_class="",
            instantiated_objects=[],
            intro=True
        )
