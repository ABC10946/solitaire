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
    backhiRaw = [["FF", "C7", "DC", "DH", "C6"], # left 0が手前 4が奥側
              ["C1", "DC", "B8", "B9", "B1"],
              ["K1", "DH", "B3", "K3", "K6"],
              ["DH", "DH", "B4", "K4", "K5"],
              ["DD", "C4", "C8", "B7", "C3"],
              ["B6", "K3", "K9", "DC", "DC"],
              ["B2", "C9", "C5", "DD", "K2"],
              ["B5", "DD", "K7", "DD", "K2"]]   # right

    backHiConverted = [[convertToHiClass(x) for x in a] for a in backhiRaw]

    game = Solitaire(backHiConverted)
    # control(game,     pickHiX=None, pickLeft=None, targetX=None, targetCenter=None, targetLeft=None, targetRight=None)
    # game.printField()
    control(game, 0, None, None, True, None, None)
    game.printField()
    control(game, 1, None, None, None, None, 0)
    game.printField()
    control(game, 2, None, None, None, None, 1)
    game.printField()
    print("=======solver======")

    # Node(parent, game, controlArr, children=[], depth=0, dead=False):
    node = Node(None, game, [None, None, None, None, None, None, None, None], [], depth=0, dead=False)

    solver = Solver()
    node = solver.solver(node)
    print("clear!!")

    print(node.getCleared())

    nodeArr = []

    while node.parent is not None:
        nodeArr.append(node)
        node = node.parent

    node = reversed(nodeArr)

    for n in node:
        # print(n.controlArr)
        # n.controlArrを人間に分かりやすい形に変換
        controlArr = n.controlArr
        if controlArr[0] is not None:
            if controlArr[2] is not None:
                if controlArr[6] is not None:
                    print("pick from hiX: " + str(controlArr[0]) + " to targetX: " + str(controlArr[2]) + " length: " + str(controlArr[6]))
                else:
                    print("pick from backhiX: " + str(controlArr[0]) + " to targetX: " + str(controlArr[2]))

            elif controlArr[3] is not None:
                print("pick from backhiX: " + str(controlArr[0]) + " to targetCenter")
            elif controlArr[4] is not None:
                print("pick from backhiX: " + str(controlArr[0]) + " to targetLeft:" + str(controlArr[4]))
            elif controlArr[5] is not None:
                print("pick from backhiX: " + str(controlArr[0]) + " to targetRight:" + str(controlArr[5]))
        elif controlArr[1] is not None:
            if controlArr[2] is not None:
                print("pick from left: " + str(controlArr[1]) + " to targetX: " + str(controlArr[2]))
            elif controlArr[3] is not None:
                print("pick from left: " + str(controlArr[1]) + " to targetCenter")
            elif controlArr[4] is not None:
                print("pick from left: " + str(controlArr[1]) + " to targetLeft:" + str(controlArr[4]))
            elif controlArr[5] is not None:
                print("pick from left: " + str(controlArr[1]) + " to targetRight:" + str(controlArr[5]))
        elif controlArr[7] is not None:
            print("clearDragon")

        n.game.printField()



if __name__ == "__main__":
    main()
