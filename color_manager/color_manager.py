import json

class Color:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class ColorPalette:
    def __init__(self, name):
        self.name = name
        self.colors = []

    def add_color(self, name, value):
        color = Color(name, value)
        self.colors.append(color)

    def to_css(self):
        css = ''
        for color in self.colors:
            css += f".{color.name} {{ color: {color.value}; }}\n"
        return css

    def to_json(self):
        data = {'name': self.name, 'colors': {}}
        for color in self.colors:
            data['colors'][color.name] = color.value
        return json.dumps(data)