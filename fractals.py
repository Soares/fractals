class ColorWheel:
    RED, YELLOW, GREEN, TEAL, BLUE, PURPLE = range(6)

    # These modes are (color, channel, direction) tuples
    # used to initialize the internal state from a given color
    # For example, at 'red', the color is (255, 0, 0) and we are
    # going towards yellow, so green (channel 1) is increasing (+1)
    # then at yellow we are going towards green, so red (channel 0)
    # is decreasing (-1), and so on.
    __modes = {
        'red': ((255, 0, 0), 1, 1),
        'yellow': ((255, 255, 0), 0, -1),
        'green': ((0, 255, 0), 2, 1),
        'teal': ((0, 255, 255), 1, -1),
        'blue': ((0, 0, 255), 0, 1),
        'purple': ((255, 0, 255), 2, -1),
    }

    def __init__(self, color=RED, brightness=1, mode=255):
        self.max = mode if mode in (1.0, 255) else 255
        self.goto(color, brightness)

    def clamp(self, n):
        """
        Return n or the closest value that is a valid color
        given our color mode
        """
        return min(self.max, max(0, n))

    def goto(self, color=None, brightness=None):
        """
        You may set color as a string from __modes (not case sensitive)
        or by passing in a new color tuple.
        You may change brightness by passing in a new brightness between
        0 and 1
        """
        if isinstance(color, str) and color.lower() in self.__modes:
            color, self.channel, self.direction = self.__modes[color.lower()]
            self.__color = list(color)
        elif isinstance(color, tuple):
            self.__color = list(map(self.clamp, color[:3]))
        if brightness is not None:
            self.brightness = min(1, max(0, brightness))
        return self.color

    @property
    def color(self):
        return tuple(map(lambda c: c * self.brightness, self.__color))

    def rotate(self, amount):
        current = self.__color[self.channel]
        if current == self.max and self.direction > 0:
            self.direction *= -1
            self.channel = (self.channel - 1) % 3
        elif current == 0 and self.direction < 0:
            self.direction *= -1
            self.channel = (self.channel + 2) % 3
        delta = self.direction * amount
        self.__color[self.channel] = self.clamp(current + delta)
        return self.color


def lindenmayer(axiom, rules):
    """
    Given a start axiom (string) and a set of rules (dictionary),
    generate the steps of the Lindenmayer System described.

    >>> dragon = lindenmayer('FX', {
    ...     'X': 'X+YF',
    ...     'Y': 'FX-Y',
    ... })
    >>> dragon.next()
    'FX'
    >>> dragon.next()
    'FX+YF'
    >>> dragon.next()
    'FX+YF+FX-YF'
    >>> dragon.next()
    'FX+YF+FX-YF+FX+YF-FX-YF'

    Note: any keys in the "rules" dictionary must be uppercase
    """
    rules = rules.items()

    def apply_rule(axiom, (symbol, replacement)):
        return axiom.replace(symbol, replacement.lower())

    while True:
        yield axiom
        axiom = reduce(apply_rule, rules, axiom).upper()


class GeneratorList(object):
    """
    Allows indexing of a generator

    >>> g = GeneratorList(i for i in range(10))
    >>> g[2]
    2
    """
    def __init__(self, generator):
        self.__generator = generator
        self.__list = []

    def __getitem__(self, index):
        for _ in range(index - len(self.__list) + 1):
            self.__list.append(self.__generator.next())
        return self.__list[index]


class LSystem(GeneratorList):
    """
    A class capable of actually doing something with L-System iteration strings
    made from lendenmayer.

    The drawing is done by looking up each character in the object's "action"
    dictionary. By default, the following actions are expected to be defined by
    implementors:

    forward: called on the character 'F'. Draw one line
    right: called on the charcater '+'. Turn right by the object's "angle"
    left: called on the character '-'. Turn left by the object's "angle"
    go: called on the charater 'G'. Move forward, without drawing a line
    save: called on the character '['. Save the current drawing state in
          the object's "states" list
    restore: called on the character ']'. Restore the drawing state from
             the object's "states" list.
    """
    def __init__(self, turtle, start, rules, angle, heading=0):
        self.turtle = turtle
        self.states = []
        self.angle = angle
        self.heading = heading
        self.actions = {
            'F': self.forward,
            '+': self.right,
            '-': self.left,
            'G': self.go,
            '[': self.save,
            ']': self.restore,
        }
        super(LSystem, self).__init__(lindenmayer(start, rules))

    def forward(self):
        self.turtle.forward(self.size)

    def right(self):
        self.turtle.right(self.angle)

    def left(self):
        self.turtle.left(self.angle)

    def go(self):
        self.turtle.up()
        self.turtle.forward(self.size)
        self.turtle.down()

    def save(self):
        x, y = self.turtle.xcor(), self.turtle.ycor()
        h, c = self.turtle.heading(), self.turtle.pencolor()
        self.states.append((x, y, h, c))

    def restore(self):
        turtle.up()
        x, y, h, c = self.states.pop()
        turtle.setx(x)
        turtle.sety(y)
        turtle.setheading(h)
        turtle.pencolor(c)
        turtle.down()

    def update(self):
        pass

    def draw(self, index, size=1):
        self.turtle.setheading(self.heading)
        self.size = size

        for char in self[index]:
            if char in self.actions:
                self.update()
                self.actions[char]()


class Dragon(LSystem):
    def __init__(self, turtle):
        super(Dragon, self).__init__(turtle, 'FX', {'X': 'X+YF', 'Y': 'FX-Y'}, 90)
        self.colors = ColorWheel('purple')
        self.__cap, self.__current = 1, 0

    def update(self):
        if self.__cap == self.__current:
            self.__cap *= 2
            self.turtle.pencolor(self.colors.rotate(40))
        self.__current += 1

    def draw(self, *args, **kwargs):
        self.turtle.pencolor(self.colors.color)
        super(Dragon, self).draw(*args, **kwargs)


if __name__ == '__main__':
    import sys
    from turtle import Turtle
    turtle = Turtle()
    turtle.hideturtle()
    turtle.speed('fastest')
    turtle.screen.colormode(255)
    turtle.up()
    turtle.setposition(-200, 200)
    turtle.down()

    fractals = {
        'snowflake': LSystem(turtle, 'F++F++F', {'F': 'F-F++F-F'}, 60),
        'dragon': LSystem(turtle, 'FX', {'X': 'X+YF', 'Y': 'FX-Y'}, 90),
        'plant': LSystem(turtle, 'FX', {'X': 'F-[[X]+X]+F[+FX]-X', 'F': 'FF'}, 25),
        'serpinsky': LSystem(turtle, 'FA', {'FA': 'FB-FA-FB', 'FB': 'FA+FB+FA'}, 60),
        'colored_dragon': Dragon(turtle),
    }

    name, num = sys.argv[1], int(sys.argv[2])
    fractals[name].draw(num)
    turtle.screen.getcanvas().postscript(file='%s-%s.ps' % (name, num))

    turtle.screen.exitonclick()
