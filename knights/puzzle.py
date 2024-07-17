from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # In the truth table, I needed an xor operation and for that is (A and B) and NOT(A and B)
    # this allows me to be able to filter some true cases to the ones I need
    # then I just use an and gate to get the true value which gives "A is a Knave"

    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), AKnave

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Having deduced that A is a knave and B is a knight
    # I need to correctly use the logical gates and get this information through
    Or(AKnave, BKnave), And(Not(BKnave), BKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    And(Or(AKnave, BKnave), And(AKnave, BKnight))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # And(AKnight, AKnave), And(And(Not(BKnave), BKnight), And(Not(CKnight), CKnave))
    And(Or(AKnave, AKnight), AKnave), CKnave, BKnight
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
