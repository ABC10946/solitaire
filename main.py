import copy
from solitaire import Solitaire, Hi
from solver import Node, Solver


def convertToHiClass(hiInput):
    if len(hiInput) != 2:
        return None

    hiHeaderKeys = ["B", "C", "K", "D", "F"]

    if hiInput[0] not in hiHeaderKeys:
        return None

    if hiInput == "DC":
        return Hi("chu")
    elif hiInput == "DH":
        return Hi("hatu")
    elif hiInput == "DD":
        return Hi("card")
    elif hiInput == "FF":
        return Hi("flower")
    else:
        num = int(hiInput[1])

        if hiInput[0] == "B":
            return Hi("bamboo", num)
        elif hiInput[0] == "C":
            return Hi("circle", num)
        elif hiInput[0] == "K":
            return Hi("kanji", num)


def printHi(hi):
    if hi is None:
        return "  "
    elif   hi.hiType == "bamboo":
        return "B" + str(hi.num)
    elif hi.hiType == "circle":
        return "C" + str(hi.num)
    elif hi.hiType == "kanji":
        return "K" + str(hi.num)
    elif hi.hiType == "chu":
        return "DC"
    elif hi.hiType == "hatu":
        return "DH"
    elif hi.hiType == "card":
        return "DD"
    elif hi.hiType == "flower":
        return "FF"
    elif hi.hiType == "disable":
        return "NO"


controlArr = []
def control(game, pickHiX, pickLeft, targetX, targetCenter, targetLeft, targetRight, length=None):
    if game.control(pickHiX, pickLeft, targetX, targetCenter, targetLeft, targetRight, length) != 0:
        print("fail")
        return -1
    else:
        controlArr.append([pickHiX, pickLeft, targetX, targetCenter, targetLeft, targetRight, length])
        return 0

def clearDragons(game):
    if game.clearDragon() == 0:
        controlArr.append(["clearDragon"])
        return 0
    else:
        return -1
    


def main():
    backhiRaw = [["B6", "DD", "DD", "FF", "B2"], # left 0が手前 4が奥側
              ["B8", "DC", "B1", "C6", "K2"],
              ["DC", "B5", "C9", "C8", "K1"],
              ["DC", "C3", "K3", "B3", "DH"],
              ["C2", "DC", "DD", "K7", "K9"],
              ["K8", "B9", "DD", "DH", "K6"],
              ["DH", "C5", "DH", "B7", "C4"],
              ["B4", "C7", "C1", "K5", "K4"]]   # right

    backHiConverted = [[convertToHiClass(x) for x in a] for a in backhiRaw]

    game = Solitaire(backHiConverted)
    # control(game,     pickHiX=None, pickLeft=None, targetX=None, targetCenter=None, targetLeft=None, targetRight=None)
    game.printField()
    control(game, 7, None, None, None, 2, None)
    game.printField()
    control(game, 7, None, 5, None, None, None)
    game.printField()
    control(game, 7, None, None, None, None, 0)
    game.printField()
    control(game, 4, None, None, None, None, 0)
    game.printField()
    control(game, 0, None, 5, None, None, None)
    game.printField()
    control(game, 7, None, 5, None, None, None)
    game.printField()
    control(game, None, 2, 5, None, None, None)
    game.printField()
    control(game, 7, None, None, None, 2, None)
    game.printField()
    control(game, 5, None, 7, None, None, None)
    game.printField()
    control(game, 4, None, None, None, 1, None)
    game.printField()
    control(game, 1, None, None, None, 0, None)
    game.printField()

    game.clearDragon()
    game.printField()

    control(game, 1, None, None, None, None, 1)
    game.printField()

    control(game, 2, None, 1, None, None, None)
    game.printField()
    
    control(game, None, 2, 1, None, None, None)
    game.printField()

    control(game, None, 0, 2, None, None, None)
    game.printField()

    control(game, 4, None, None, None, 0, None)
    game.printField()

    control(game, 0, None, None, None, 2, None)
    game.printField()

    game.clearDragon()
    game.printField()

    control(game, 0, None, None, True, None, None)
    game.printField()

    control(game, 0, None, None, None, None, 1)
    game.printField()

    control(game, 1, None, 4, None, None, None)
    game.printField()

    control(game, 4, None, 2, None, None, None)
    game.printField()

    control(game, 2, None, 0, None, None, None)
    game.printField()

    control(game, 2, None, 4, None, None, None)
    game.printField()

    control(game, 2, None, None, None, None, 2)
    game.printField()

    control(game, 1, None, None, None, None, 2)
    game.printField()

    control(game, 3, None, None, None, None, 0)
    game.printField()

    control(game, 3, None, None, None, None, 2)
    game.printField()

    control(game, 3, None, None, None, None, 1)
    game.printField()

    control(game, 0, None, None, None, None, 2)
    game.printField()

    control(game, 7, None, None, None, None, 1)
    game.printField()

    control(game, 0, None, 4, None, None, None, 3)
    game.printField()

    control(game, 7, None, 0, None, None, None, 3)
    game.printField()

    control(game, 6, None, None, None, 2, None)
    game.printField()

    # control(game, 6, None, 2, None, None, None)
    # game.printField()

    # game.clearDragon()
    # game.printField()

    # control(game, 5, None, 6, None, None, None)
    # game.printField()

    # control(game, 6, None, 7, None, None, None)
    # game.printField()
    
    print("=======solver======")


    # while not solver(game):
    #     game.printField()

    # Node(parent, game, controlArr, children=[], depth=0, dead=False):
    node = Node(None, game, [None, None, None, None, None, None, None, None], [], depth=0, dead=False)

    solver = Solver()
    solver.solver(node)
    print("clear!!")

    while True:
        print(node.controlArr)
        print(len(node.children))
        node.run()
        node.game.printField()
        if len(node.children) != 0:
            node = node.children[0]
        else:
            break


if __name__ == "__main__":
    main()
