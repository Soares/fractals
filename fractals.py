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
    def __init__(self, axiom, rules, angle, heading=0):
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
        super(LSystem, self).__init__(lindenmayer(axiom, rules))

    def draw(self, index):
        for char in self[index]:
            if char in self.actions:
                self.actions[char]()
