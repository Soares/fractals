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
