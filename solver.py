import copy
from collections import deque

dragons = ["chu", "hatu", "card", "flower", "disable"] # disableは三元牌４つそろったときleft3の埋める時に用いる

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

class Solver:
    def __init__(self):
        self.visited_states = set()

    def solver(self, root): # 終了したらTrueを返す
        stack = deque([root])
        while stack:
            node = stack.pop()

            if node.getCleared() and node.parent is not None:
                node.parent.setCleared()
                node.parent.chlideren = []
                node.parent.children.append(node)
                continue

            if sum([len(x) for x in node.game.backhi]) == 0:
                print("====clear====")
                node.setCleared()
                node.parent.children = []
                node.parent.children.append(node)
                node.parent.setCleared()
                return node

            if node.run() == -1:
                node.dead = True
 
                continue

            if node.parent is not None:
                node.parent.children.append(node)

            state = (tuple(tuple(x) for x in node.game.backhi), tuple(node.game.left3), tuple(node.game.right3), node.game.center)
            if state in self.visited_states:
                continue

            self.visited_states.add(state)

            if node.parent is not None and node.parent.parent is not None:
                grandNode = node.parent.parent
                if grandNode.game.backhi == node.game.backhi and grandNode.game.left3 == node.game.left3 and grandNode.game.right3 == node.game.right3:
                    print("------------grand match----------------")
                    node.dead = True
                    continue

            controlArrs = []

            # もし手元牌の位置番手前で、その次に三元牌があるときは、その三元牌を移動させるために、手元牌を移動させる
            for pickHiX in range(8):
                if len(node.game.backhi[pickHiX]) > 1:
                    if node.game.backhi[pickHiX][1].hiType:
                        for targetX in range(8):
                            if pickHiX != targetX:
                                controlArrs.append([pickHiX, None, targetX, None, None, None, None, None])

                        for targetLeft in range(3):
                            controlArrs.append([pickHiX, None, None, None, targetLeft, None, None, None])

            for pickHiX in range(8):
                for targetRight in range(3):
                    controlArrs.append([pickHiX, None, None, None, None, targetRight, None, None])

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

            controlArrs = reversed(controlArrs)

            for i in controlArrs:
                node_ = Node(node, copy.deepcopy(node.game), i, children=[], depth=node.depth + 1, dead=False)
                stack.append(node_)

        return root
