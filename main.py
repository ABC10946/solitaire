import copy

hiTypes = ["bamboo", "circle", "kanji", "chu", "hatu", "card", "flower"]


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
        print(','.join([self.printHi(x) for x in self.left3]), self.printHi(self.center), ','.join([self.printHi(x) for x in self.right3]))
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


    def control(self, pickHiX=None, pickLeft=None, pickRight=None, targetX=None, targetCenter=None, targetLeft=None, targetRight=None): # backhi(手元手札)の左からX列目の一番手前の牌(操作できる牌)を移動先の列targetXまたはleft3 (top-left), right3 (top-right)に移動させる。移動できない場合は-1を返す
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
        if pickHiX is not None and pickLeft is not None and pickRight is not None:
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
            
            pickHi = self.left3[pickLeft]

            afterLeft3[pickLeft] = None


        elif pickRight is not None:
            if pickRight > 2:
                print("pickRight should be below 3")
                return -1
            
            pickHi = self.right3[pickLeft]

            afterRight3[pickRight] = None

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

            # stackableか判定する
            targetHeadHi = self.backhi[targetX][0]
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
            elif pickRight is not None:
                self.right3 = afterRight3

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

            self.left3[targetLeft] = pickHi

            if pickHiX is not None:
                self.backhi[pickHiX] = afterPickedHiXArray
            elif pickRight is not None:
                self.right3 = afterRight3
            
            return 0
        elif targetRight is not None:
            print("right control")
            if targetRight > 2:
                print("targetRight should below 3")
                return -1

            self.right3[targetRight] = pickHi

            
            if pickHiX is not None:
                self.backhi[pickHiX] = afterPickedHiXArray
            elif pickLeft is not None:
                self.left3 = afterLeft3
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


def main():
    backhiRaw = [["C5", "DD", "DD", "B4", "K8"],
              ["DH", "K6", "K5", "DH", "C4"],
              ["B2", "K7", "K1", "B5", "DH"],
              ["DC", "DD", "C8", "DD", "K4"],
              ["B3", "B6", "DC", "C1", "C2"],
              ["DC", "B7", "C7", "B9", "K9"],
              ["FF", "C3", "K2", "DC", "B8"],
              ["DH", "K3", "B1", "C9", "C6"]]

    backHiConverted = [[convertToHiClass(x) for x in a] for a in backhiRaw]

    game = Solitaire(backHiConverted)
    # control(pickHiX=None, pickLeft=None, pickRight=None, targetX=None, targetCenter=None, targetLeft=None, targetRight=None)
    if game.control(6, None, None, None, True) != 0:
        print("fail")

    # fail
    # if game.control(4, 6) != 0:
    #     print("fail")
    # else:
    #     print("success")

    if game.control(2, None, None, None, None, 0) != 0:
        print("fail")

    if game.control(None, 0, None, 6, None, None) != 0:
        print("fail")

    if game.control(4, None, None, None, None, 0) != 0:
        print("fail")

    if game.control(4, None, None, 2, None, None) != 0:
        print("fail")

    if game.control(0, None, None, 2, None, None) != 0:
        print("fail")

    game.printField()


if __name__ == "__main__":
    main()
