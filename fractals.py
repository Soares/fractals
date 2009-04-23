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
    'FX+YF+FX+YF-YF'
    >>> dragon.next()
    'FX+YF+FX+YF-YF+FX+YF+FX+YF-YF-FX+YF-YF'

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
