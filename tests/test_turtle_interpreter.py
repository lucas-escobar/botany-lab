import unittest
from pathlib import Path
import lindenmayer_system as ls
from PIL import Image, ImageDraw


class TurtleInterpreterTestCase(unittest.TestCase):
    def setUp(self):
        self.image = Image.new("RGB", (1280, 1280), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.pos = (1280 / 2, 1280 / 2, 180)
        self.step_length = 10
        self.turn_angle = 90
        self.turtle = ls.TurtleInterpreter(
            self.pos[0], self.pos[1], self.pos[2], self.step_length, self.turn_angle
        )
        tests_dir = Path(__file__).resolve().parent
        self.output_dir = tests_dir / "testing_outputs"
        self.alphabet = {"F", "f", "+", "-"}

    def test_interpret(self):
        axiom = "F-F-F-F"
        production_rules = {"F": "F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF", "f": "fffff"}
        derivation_length = 2
        draw_color = (0, 0, 0)
        output_file = self.output_dir / "interpret_test_output.jpg"

        lsystem = ls.DOLSystem(self.alphabet, axiom, production_rules)
        lsystem_strings = lsystem.apply_production_rules(derivation_length)
        lsystem_string = lsystem_strings[-1]

        instructions = self.turtle.interpret(lsystem_string)

        for instruction in instructions:
            point1 = (instruction[1][1], instruction[1][0])
            point2 = (instruction[2][1], instruction[2][0])
            if instruction[0] == "line":
                self.draw.line((point1, point2), fill=draw_color, width=2)

        self.image.save(output_file)

    def test_interpret_FASS(self):
        alphabet = {"Fl", "Fr", "+", "-"}
        axiom = "Fl"
        production_rules = {
            "Fl": "FlFl+Fr+Fr-Fl-Fl+Fr+FrFl-Fr-FlFlFr+Fl-Fr-FlFl-Fr+FlFr+Fr+Fl-Fl-FrFr+",
            "Fr": "-FlFl+Fr+Fr-Fl-FlFr-Fl+FrFr+Fl+Fr-FlFrFr+Fl+FrFl-Fl-Fr+Fr+Fl-Fl-FrFr",
        }
        derivation_length = 3
        draw_color = (0, 0, 0)
        output_file = self.output_dir / "interpret_fass_test_output.jpg"

        lsystem = ls.DOLSystem(alphabet, axiom, production_rules)
        lsystem_strings = lsystem.apply_production_rules(derivation_length)
        lsystem_string = lsystem_strings[-1]

        instructions = self.turtle.interpret(lsystem_string)

        for instruction in instructions:
            point1 = (instruction[1][1], instruction[1][0])
            point2 = (instruction[2][1], instruction[2][0])
            if instruction[0] == "line":
                self.draw.line((point1, point2), fill=draw_color, width=2)

        self.image.save(output_file)

    def test_interpret_bracketed(self):
        self.turtle.turn_angle = 25.7
        alphabet = {"F", "+", "-", "[", "]"}
        axiom = "F"
        production_rules = {"F": "F[+F]F[-F]F"}
        derivation_length = 5
        draw_color = (0, 0, 0)
        output_file = self.output_dir / "interpret_bracketed_test_output.jpg"

        lsystem = ls.DOLSystem(alphabet, axiom, production_rules)
        lsystem_strings = lsystem.apply_production_rules(derivation_length)
        lsystem_string = lsystem_strings[-1]

        instructions = self.turtle.interpret(lsystem_string)

        for instruction in instructions:
            point1 = (instruction[1][1], instruction[1][0] + 600)
            point2 = (instruction[2][1], instruction[2][0] + 600)
            if instruction[0] == "line":
                self.draw.line((point1, point2), fill=draw_color, width=2)

        self.image.save(output_file)


if __name__ == "__main__":
    unittest.main()
