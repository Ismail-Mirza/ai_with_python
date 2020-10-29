from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
initital0 = And(AKnight,AKnave)
knowledge0 = And(
    # TODO
    #each person is a Knight or Knave
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Or(CKnight,CKnave),
    #a person either a Knight or a Knave but not both
    Not(And(AKnight,AKnave)),
    Not(And(BKnight,BKnave)),
    Not(And(CKnight,CKnave)),
    #initial what a knight say is true but what a knave say is false
    Implication(AKnight,initital0),
    Implication(AKnave,Not(initital0))

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
initial1=And(AKnave,BKnave)
knowledge1 = And(
        #each person is a Knight or Knave
        Or(AKnight,AKnave),
        Or(BKnight,BKnave),
        Or(CKnight,CKnave),
        #a person either a Knight or a Knave but not both
        Not(And(AKnight,AKnave)),
        Not(And(BKnight,BKnave)),
        Not(And(CKnight,CKnave)),
        Implication(AKnight,initial1),
        Implication(AKnave,Not(initial1))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
initial2A=Or(And(AKnight,BKnight),And(AKnave,BKnave))
initial2B = Or(And(AKnight,BKnave),And(AKnave,BKnight))
knowledge2 = And(
    # TODO
            #each person is a Knight or Knave
            Or(AKnight,AKnave),
            Or(BKnight,BKnave),
            Or(CKnight,CKnave),
            #a person either a Knight or a Knave but not both
            Not(And(AKnight,AKnave)),
            Not(And(BKnight,BKnave)),
            Not(And(CKnight,CKnave)),
            Implication(AKnight,initial2A),
            Implication(AKnave,Not(initial2A)),
            Implication(BKnight,initial2B),
            Implication(BKnave,Not(initial2B))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
a = Or(AKnight,AKnave)
b = And(Biconditional(AKnave,BKnight),CKnave)
c = AKnight
knowledge3 = And(
    # TODO
    #each person is a Knight or Knave
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Or(CKnight,CKnave),
    #a person either a Knight or a Knave but not both
    Not(And(AKnight,AKnave)),
    Not(And(BKnight,BKnave)),
    Not(And(CKnight,CKnave)),
    Biconditional(AKnight,a),
    Biconditional(BKnight,b),
    Biconditional(CKnight,c)

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
