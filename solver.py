import copy

class Node:
    def __init__(self, parent, game, controlArr, children=[], depth=0, dead=False):
        self.game = game
        self.controlArr = controlArr
        self.children = children
        self.parent = parent
        self.depth = depth
        self.dead = dead
        self.cleared = False

    def setCleared(self):
        self.cleared = True

    def getCleared(self):
        return self.cleared

    def run(self):
        res = None
        if self.controlArr[7]:
            res = self.game.clearDragon()
        else:
            res = self.game.control(self.controlArr[0], self.controlArr[1], self.controlArr[2], self.controlArr[3], self.controlArr[4], self.controlArr[5], self.controlArr[6])

        if res != 0:
            return -1
        else:
            return 0


def solver(node): # 終了したらTrueを返す
    if sum([len(x) for x in node.game.backhi]) == 0:
        print("====clear====")
        node.setCleared()
        return node

    if node.run() == -1:
        node.dead = True
        return node
    
    if node.parent is not None and node.parent.parent is not None:
        grandNode = node.parent.parent
        if grandNode.game.backhi == node.game.backhi and grandNode.game.left3 == node.game.left3 and grandNode.game.right3 == node.game.right3:
            print("------------grand match----------------")
            node.dead = True
            return node

    controlArrs = []
    controlArrs.append([None, None, None, None, None, None, None, True])

    # 手元牌からの移動
    for pickHiX in range(8):
        for targetX in range(8):
            for length in range(1, 10):
                if pickHiX != targetX:
                    controlArrs.append([pickHiX, None, targetX, None, None, None, None, length])

    for pickHiX in range(8):
        for targetLeft in range(3):
            controlArrs.append([pickHiX, None, None, None, targetLeft, None, None, None])

    for pickHiX in range(8):
        for targetRight in range(3):
            controlArrs.append([pickHiX, None, None, None, None, targetRight, None, None])

    for pickHiX in range(8):
        controlArrs.append([pickHiX, None, None, True, None, None, None, None])


    # left3からの移動
    for pickLeft in range(3):
        for targetX in range(8):
            controlArrs.append([None, pickLeft, targetX, None, None, None, None, None])

    for pickLeft in range(3):
        for targetRight in range(3):
            controlArrs.append([None, pickLeft, None, None, None, targetRight, None, None])

    for pickLeft in range(3):
        controlArrs.append([None, pickLeft, None, None, True, None, None, None])

    for i in controlArrs:
        node_ = Node(copy.deepcopy(node), copy.deepcopy(node.game), i, children=[], depth=node.depth + 1, dead=False)
        node_ = solver(node_)

        if node_.getCleared():
            node.children.append(node_)
            node.setCleared()
            return node

    return node