""" This module contains classes and functions to generate and render Lindenmayer systems."""

# Setup

## standard library
import itertools
import typing
import collections

## external
import numpy as np
from PIL import Image, ImageDraw


# Types


Degrees = typing.NewType("Degrees", float)
Letter = typing.NewType("Letter", typing.Union(str, Edge, Node))
Word = typing.NewType("Word", typing.List[Letter])

Point = collections.namedtuple("Point", ("x", float), ("y", float))

Direction = collections.namedtuple("Direction", ("dx", float), ("dy", float))

TurtlePosition2D = collections.namedtuple(
    "TurtlePosition2D", [("x", float), ("y", float), ("heading", Degrees)]
)

TurtlePosition3D = collections.namedtuple(
    "TurtlePosition3D", [("x", float), ("y", float), ("z", float), ("heading", Degrees)]
)

Edge = collections.namedtuple("Edge", ("symbol", str), ("type", str))

Node = collections.namedtuple(
    "Node",
    ("symbol", str),
    ("entry", typing.Tuple(Point, Direction)),
    ("exit", typing.Tuple(Point, Direction)),
    ("frame", str),
)

RuleParameters = collections.namedtuple(
    "RuleParameters",
    [
        ("predecessor", Letter),
        ("successor", typing.Union[Letter, typing.List[Letter]]),
        ("probabilities", typing.List[float]),
        ("is_stochastic", bool),
    ],
)

RuleSetParameters = collections.namedtuple(
    "RuleSetParameters",
    [
        ("rules", typing.List[ProductionRule]),
    ],
)

LSystemParameters = collections.namedtuple(
    "LSystemParameters",
    [
        ("alphabet", typing.List[Letter]),
        ("axiom", Word),
        ("production_rules", ProductionRuleSet),
    ],
)

TurtleInterpreterParameters = collections.namedtuple(
    "TurtleInterpreterParameters",
    [
        ("position", typing.Union(TurtlePosition2D, TurtlePosition3D)),
        ("step_length", float),
        ("turn_angle", Degrees),
    ],
)


# Classes


class ProductionRule:
    def __init__(self, data: RuleParameters):
        for attr, value in data._asdict.items():
            setattr(self, attr, value)

    def generate_successor(self):
        if self.is_stochastic:
            return np.random.choice(self.successor, self.probabilities)
        else:
            return self.successor


class ProductionRuleSet:
    def __init__(self, data: RuleSetParameters):
        for attr, value in data._asdict.items():
            setattr(self, attr, value)

    # Public
    def apply_to(self, word: Word) -> Word:
        new_word = []
        for letter in word:
            if letter in self._get_predecessors():
                new_word.append(self.rules._asdict[letter].generate_successor())
            else:
                new_word.append(letter)
        return new_word

    def add(self, rule: ProductionRule):
        self.rules.append(rule)

    # Private
    def _get_predecessors(self):
        return [rule.predecessor for rule in self.rules]


class DOLSystem:
    """A string-based, deterministic, context-free Lindenmayer system."""

    def __init__(self, data: LSystemParameters):
        for attr, value in data._asdict.items():
            setattr(self, attr, value)

    def apply_production_rules(self, derivation_length: int):
        dev_words = [self.axiom]
        for _ in range(derivation_length):
            new_word = self.production_rules.apply_to(dev_words[-1])
            dev_words.append(new_word)
        return developmental_words

    def _parse_commands(self, command_string):
        """Checks for two char commands"""
        commands = []
        for i, char in enumerate(command_string):
            if char == "F" and i + 1 < len(command_string):
                next_char = command_string[i + 1]
                if next_char == "l":
                    commands.append("Fl")
                elif next_char == "r":
                    commands.append("Fr")
                else:
                    commands.append("F")
            elif char != "l" and char != "r":
                commands.append(char)
        return commands


class TurtleInterpreter:
    def __init__(self, data: TurtleInterpreterParameters):
        for attr, value in data._asdict.items():
            setattr(self, attr, value)
        self.state_stack = []
        self.instructions = []
        self.pen_down = True

    def forward(self):
        new_x = self.position.x + self.step_length * np.cos(
            np.radians(self.position.heading)
        )
        new_y = self.position.y + self.step_length * np.sin(
            np.radians(self.position.heading)
        )
        new_position = TurtlePosition2D(new_x, new_y, self.position.heading)
        if self.pen_down:
            self.instructions.append(
                (
                    "line",
                    (self.position.x, self.position.y),
                    (new_position.x, new_position.y),
                )
            )
        self.position = new_position

    def rotate(self, degrees):
        new_angle = (self.position.heading + degrees) % 360
        self.position = (self.position.x, self.position.y, new_angle)

    def interpret(self, lsystem_string):
        for char in lsystem_string:
            if char == "F":
                self.forward()
            elif char == "f":
                self.pen_down = False
                self.forward()
                self.pen_down = True
            elif char == "+":
                self.rotate(self.turn_angle)
            elif char == "-":
                self.rotate(-self.turn_angle)
            elif char == "[":
                self.state_stack.append(self.position)
            elif char == "]":
                self.position = self.state_stack.pop()
        return self.instructions


class ImageProcessor:
    def __init__(self, width, height, output_file, bg_color):
        self.output_file = output_file
        self.image = Image.new("RGB", (width, height), bg_color)

    def draw_line(self, x1, y1, x2, y2, color=(0, 0, 0), width=1):
        ImageDraw.Draw(self.image).line([(x1, y1), (x2, y2)], fill=color, width=width)

    def save_image(self):
        self.image.save(self.output_file)


def generate_all_words(alphabet, max_word_length):
    all_words = []
    min_word_size = 1
    for word_length in range(min_word_size, max_word_length + 1):
        for permutation in itertools.permutations(alphabet, word_length):
            all_words.append("".join(permutation))
    return all_words
