module Fractals where
import Prelude
import Data.String.Utils(replace)
import Char(toLower, toUpper)

upper = map toUpper
lower = map toLower

type Symbol = Char
type Axiom = [Symbol]
type Rules = [(Symbol, Axiom)]

-- Given an axiom and a set of rules, generate a list including this
-- axiom and all future axioms in the described Lindenmayer System.
-- Note that each symbol in the rules should be uppercase.
lindenmayer :: Axiom -> Rules -> [Axiom]
lindenmayer axiom rules = axiom : lindenmayer next rules where
    apply_rule axiom (symbol, new) = replace [symbol] (lower new) axiom
    next = upper $ foldl apply_rule axiom rules
