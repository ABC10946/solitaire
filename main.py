import copy

hiTypes = ["bamboo", "circle", "kanji", "chu", "hatu", "card", "flower"]
dragons = ["chu", "hatu", "card", "flower", "disable"] # disableは三元牌４つそろったときleft3の埋める時に用いる


class Hi:
    def __init__(self, hiType, num=None):
        if hiType in hiTypes:
            self.hiType = hiType
            self.num = num

        else:
            print("Error, " + hiType + " is not hiTypes")


class Solitaire:
    def __init__(self, backhi): # backhi is 8 length of [Hi]
        if not self._validate(backhi):
            return None

        self.left3 = [None, None, None]
        self.right3 = [None, None, None]
        self.center = None # center cell is for flower hi
        self.backhi = backhi

    def _validate(self, backhi):
        if len(backhi) != 8:
            return False

        return True
    

    def printField(self):
        print(','.join([self.printHi(x) for x in self.left3]), self.printHi(self.center), '  ', ','.join([self.printHi(x) for x in self.right3]))
        # print([[self.printHi(x) for x in a] for a in self.backhi])
        maxY = max([len(x) for x in self.backhi])
        for y in range(maxY):
            for x in range(8):
                if len(self.backhi[x]) < y + 1:
                    print('   ', end='')
                else:
                    print(self.printHi(self.backhi[x][y * -1 -1]) + ' ', end='')
        
            print()


    def printHi(self, hi):
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


    def control(self, pickHiX=None, pickLeft=None, targetX=None, targetCenter=None, targetLeft=None, targetRight=None, length=None): # backhi(手元手札)の左からX列目の一番手前の牌(操作できる牌)を移動先の列targetXまたはleft3 (top-left), right3 (top-right)に移動させる。移動できない場合は-1を返す
        # targetX = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7
        # targetCenter = True | False
        # targetLeft = 0 | 1 | 2
        # targetRight = 0 | 1 | 2

        ##############
        # validation #
        ##############

        ####################
        # 牌取得validation #
        ####################

        # pickはどれか一つしか指定できない
        if pickHiX is not None and pickLeft is not None:
            print("pick control should be only 1")
            return -1
        
        pickHi = None

        afterPickedHiXArray = []
        afterLeft3 = copy.deepcopy(self.left3)
        afterRight3 = copy.deepcopy(self.right3)
        # もし手札の方から牌を取得するなら
        if pickHiX is not None:
            if pickHiX > 7:
                print("pickHiX should below 8")
                return -1

           
            pickHi = self.backhi[pickHiX][0]

            # pickHiXで手札のX列は牌を取られるので、もし移動が可能だった場合は配列から先頭を削除する。あらかじめ削除済みの配列を作る処理。
            for i in range(len(self.backhi[pickHiX])):
                if i == 0:
                    continue
                
                afterPickedHiXArray.append(self.backhi[pickHiX][i])

        elif pickLeft is not None:
            if pickLeft > 2:
                print("pickLeft should be below 3")
                return -1

            if self.left3[pickLeft].hiType == "disable":
                print("その牌は無効化されたため使えません")
                return -1
            
            pickHi = self.left3[pickLeft]

            afterLeft3[pickLeft] = None


        ######################
        # 牌配置先validation #
        ######################

        # targetはどれか一つしか指定できない
        if targetX is not None and targetCenter is not None and targetLeft is not None and targetRight is not None:
            print("target control should be only 1")
            return -1
        


        # 配置先がどれもNoneなら何もしない
        if targetX is None and targetLeft is None and targetRight is None and targetCenter is None:
            return 0


        ###################
        # control process #
        ###################

        if targetX is not None:
            if targetX > 7:
                print("targetX should below 8")
                return -1

            if targetX == pickHiX:
                return 0

            # もしbackhiの中から移動させるときに連結させて移動できるなら
            if pickHiX is not None and self.backhi[pickHiX][0].hiType not in dragons and self._linkedTailIndex(self.backhi[pickHiX]) != 0:
                    linkedTailIndex = self._linkedTailIndex(self.backhi[pickHiX])

                    # もし移動するときのブロック長が指定されていて、それが連結しているブロックの数より少なければ移動可能
                    if length is not None and linkedTailIndex >= length:
                        linkedTailIndex = length-1

                    linkedBlock = self.backhi[pickHiX][0:linkedTailIndex+1]

                    afterPickedHiXArray = self.backhi[pickHiX][linkedTailIndex + 1:]

                    # 連結部最後尾 (連結部一番奥側)とtargetXの牌を確認してstackableか判定する
                    if self.backhi[targetX] != []:
                        targetHeadHi = self.backhi[targetX][0]
                        if linkedBlock[-1].hiType == targetHeadHi.hiType:
                            return -1
                        
                        if linkedBlock[-1].num == targetHeadHi.num:
                            return -1
                        
                        if linkedBlock[-1].num > targetHeadHi.num:
                            return -1
                    
                    # 判定が通ったら積み上げられる
                    for blockTailIndex in reversed(range(len(linkedBlock))):
                        self.backhi[targetX] = appendToHead(self.backhi[targetX], linkedBlock[blockTailIndex])

                    self.backhi[pickHiX] = afterPickedHiXArray

                    return 0
            else:
                # stackableか判定する
                if self.backhi[targetX] != []: # もし積み上げ先の牌が空でないなら判定処理を行う
                    targetHeadHi = self.backhi[targetX][0]
                    if pickHi.hiType in dragons: # もし牌が中、發、カード、または花だった場合はnot stackable
                        return -1

                    if targetHeadHi.hiType in dragons:
                        return -1

                    if pickHi.hiType == targetHeadHi.hiType: # もし牌の記号が同じならnot stackable
                        return -1

                    if pickHi.num == targetHeadHi.num: # もし牌の数字が同じならnot stackable
                        return -1

                    if pickHi.num > targetHeadHi.num: # もし積み上げ先の牌よりも今pickしてる牌の数字が大きかったら積み上げられない
                        return -1
                # それ以外なら積み上げられる



                self.backhi[targetX] = appendToHead(self.backhi[targetX], pickHi)
                if pickHiX is not None:
                    self.backhi[pickHiX] = afterPickedHiXArray
                elif pickLeft is not None:
                    self.left3 = afterLeft3

                return 0
            
        elif targetCenter: # 中央に花の牌の配置を試みる
            if pickHi.hiType == "flower":
                self.backhi[pickHiX] = afterPickedHiXArray
                self.left3 = afterLeft3
                self.right3 = afterRight3
                self.center = pickHi
                return 0
            else:
                return -1
        elif targetLeft is not None:
            if targetLeft > 2:
                print("targetLeft should below 3")
                return -1

            if self.left3[targetLeft] is None:
                self.left3[targetLeft] = pickHi
            else:
                print("targetLeft not empty")
                return -1

            if pickHiX is not None:
                self.backhi[pickHiX] = afterPickedHiXArray
            
            return 0
        elif targetRight is not None:
            if targetRight > 2:
                print("targetRight should below 3")
                return -1

            # 右側に牌を配置するときは1から同じ種類の牌がインクリメントされなければいけない
            if self.right3[targetRight] is None and pickHi.num == 1:
                self.right3[targetRight] = pickHi

            elif self.right3[targetRight].hiType == pickHi.hiType and self.right3[targetRight].num == pickHi.num - 1:
                self.right3[targetRight] = pickHi
            else:
                return -1

            
            if pickHiX is not None:
                self.backhi[pickHiX] = afterPickedHiXArray
            elif pickLeft is not None:
                self.left3 = afterLeft3
            return 0


    def _linkedTailIndex(self, hiArr): # 与えられた列のどこからどこまでが連結しているのかをインデックスで返す
        linkedTailIndex = 0

        linkedTailIndex = 0
        for i in range(len(hiArr)-1):
            if hiArr[i].hiType != hiArr[i+1].hiType and hiArr[i].num + 1 == hiArr[i + 1].num:
                linkedTailIndex = i+1
            else:
                return linkedTailIndex

        return linkedTailIndex


    def clearDragon(self):
        # left3または各列の一番手前に同じ三元牌が４つある場合はそれらを消す
        count = [0, 0, 0] # chu hatu card

        # left3にあるかの判定


        for i in self.left3:
            if i is not None:
                if i.hiType == "chu":
                    count[0] += 1
                elif i.hiType == "hatu":
                    count[1] += 1
                elif i.hiType == "card":
                    count[2] += 1

        for x in range(8):
            if len(self.backhi[x]) > 0:
                head = self.backhi[x][0].hiType
                if head == "chu":
                    count[0] += 1
                elif head == "hatu":
                    count[1] += 1
                elif head == "card":
                    count[2] += 1

        
        removableDragon = None
        if count[0] == 4:
            removableDragon = "chu"
        elif count[1] == 4:
            removableDragon = "hatu"
        elif count[2] == 4:
            removableDragon = "card"

        # left3の一つを埋める (空いていないまたは同じ牌種のものがなければ削除不可)
        if None not in self.left3 and removableDragon not in [x.hiType for x in self.left3]:
            return -1

        # print(self.left3)
        disableLeft3CellIdx = [x.hiType for x in self.left3].index(removableDragon)
        self.left3[disableLeft3CellIdx].hiType = "disable"
        
        # 三元牌削除処理
        # 4つそろってる三元牌を消す
        for i, elem in enumerate(self.left3):
            if elem is not None:
                if elem.hiType == removableDragon:
                    self.left3[i] = None

        for x in range(8):
            if len(self.backhi[x]) > 0:
                head = self.backhi[x][0].hiType
                if head == removableDragon:
                    self.backhi[x] = self.backhi[x][1:]

        
        return 0



def appendToHead(arr, element):
    afterArr = [0 for _ in range(len(arr) + 1)] # 元の配列よりも一つ要素数を増やした配列を作成

    for i in range(len(arr)):
        afterArr[i + 1] = arr[i]
    afterArr[0] = element
    return afterArr


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


def solver(solitaire):
    pass

def control(game, pickHiX, pickLeft, targetX, targetCenter, targetLeft, targetRight, length=None):
    if game.control(pickHiX, pickLeft, targetX, targetCenter, targetLeft, targetRight, length) != 0:
        print("fail")
    

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

    # should be fail
    control(game, 0, None, 4, None, None, None, 3)
    game.printField()

    control(game, 7, None, 0, None, None, None, 3)
    game.printField()

    control(game, 6, None, None, None, 2, None)
    game.printField()

    control(game, 6, None, 2, None, None, None)
    game.printField()

    game.clearDragon()
    game.printField()

    control(game, 5, None, 6, None, None, None)
    game.printField()

    control(game, 6, None, 7, None, None, None)
    game.printField()

    # clear!!

if __name__ == "__main__":
    main()
