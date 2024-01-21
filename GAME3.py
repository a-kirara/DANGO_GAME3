import pyxel

#########
## 定数
#########
MENU_MODE = 0
GAME_MODE = 1
# 画面サイズ
SCREEN_W = 200
SCREEN_H = 200
# 始点
KUSI_START_X = 100
KUSI_START_Y = 168
DANGO1_START_X = 0
DANGO1_START_Y = 100
DANGO2_START_X = 100
DANGO2_START_Y = 0
DANGO3_START_X = 40
DANGO3_START_Y = 20
DANGO4_START_X = 20
DANGO4_START_Y = 40
# イメージマップ
IMAGE_MAP = 0
# イメージマップ 団子
MARU_MAP = [
    [ 0, 0, 16, 16 ], # イメージマップ みたらし団子
    [ 24, 0, 16, 16 ], # イメージマップ 黒ゴマ団子
    [ 0, 24, 16, 16], #イメージマップ　シャボン玉
    [ 24, 24, 16, 16], #イメージマップ　風船
]
KUSI_W = 2
# イメージマップ みたらし団子 & 黒ゴマ団子 & くし
KUSI_MAP = {
    '--' : [ 55, 0, 2, 32],   # イメージマップ くし
    '0-' : [ 64, 0, 16, 32 ], # イメージマップ みたらし団子 & くし
    '1-' : [ 104, 0, 16, 32 ], # イメージマップ 黒ごま団子 & くし
    '00' : [ 80, 0, 16, 32], # 0-0 みたらし団子+みたらし団子
    '01' : [ 160, 0, 16, 32], # 0-1 みたらし団子+黒ごま団子
    '10' : [ 144, 0, 16, 32], # 1-0 黒ごま団子+みたらし団子
    '11' : [ 128, 0, 16, 32], # 1-1 黒ごま団子+黒ごま団子
}

# ヒット判定する範囲
HITY_IN = 4
LIFE = 1

class Maru:
    def __init__(self, type, maruX, maruY, maruW, maruH, vxs, vys, hit, hitMap):
        self.type = type
        self.maruX = maruX
        self.maruY = maruY
        self.maruW = maruW
        self.maruH = maruH
        self.vxs = vxs
        self.vys = vys
        self.hit = hit
        self.hitMap = hitMap

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getMaruX(self):
        return self.maruX

    def setMaruX(self, maruX):
        self.maruX = maruX

    def getMaruY(self):
        return self.maruY

    def setMaruY(self, maruY):
        self.maruY = maruY

    def getMaruW(self):
        return self.maruW

    def setMaruW(self, maruW):
        self.maruW = maruW

    def getMaruH(self):
        return self.maruH

    def setMaruH(self, maruH):
        self.maruH = maruH

    def getVxs(self):
        return self.vxs

    def setVxs(self, vxs):
        self.vxs = vxs

    def getVys(self):
        return self.vys

    def setVys(self, vys):
        self.vys = vys

    def getHit(self):
        return self.hit

    def setHit(self, hit):
        self.hit = hit

    def getHitMap(self):
        return self.hitMap

    def setHitMap(self, hitMap):
        self.hitMap = hitMap

class App:
    # 初期処理
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H)
        pyxel.load("test.pyxels.pyxres")
        self.mode = MENU_MODE
        self.init_kusi()
        self.init_dango()

        self.speed = 1.0
        self.life = 3
        self.score = 0
        self.gameover_flag = False
        self.hitStatus = '--'
    
        pyxel.run(self.update, self.draw)

    
    # くしの初期処理
    def init_kusi(self):
        self.kusi_x = KUSI_START_X
        self.kusi_y = KUSI_START_Y

    # 団子の初期処理
    def init_dango(self):
        self.maru = [
            Maru(0, DANGO1_START_X, DANGO1_START_Y, MARU_MAP[0][2], MARU_MAP[0][3], pyxel.cos(pyxel.rndi(30,150)), pyxel.sin(pyxel.rndi(30,150)), False, 0),
            Maru(1, DANGO2_START_X, DANGO2_START_Y, MARU_MAP[1][2], MARU_MAP[1][3], pyxel.cos(pyxel.rndi(30,150)), pyxel.sin(pyxel.rndi(30,150)),False, 1),
            Maru(2, DANGO3_START_X, DANGO3_START_Y, MARU_MAP[2][2], MARU_MAP[2][3], pyxel.cos(pyxel.rndi(30,150)), pyxel.sin(pyxel.rndi(30,150)),False, 2),
            Maru(3, DANGO4_START_X, DANGO4_START_Y, MARU_MAP[3][2], MARU_MAP[3][3], pyxel.cos(pyxel.rndi(30,150)), pyxel.sin(pyxel.rndi(30,150)),False, 3),
        ]

        pyxel.sound(0).set(notes='A2C3', tones='TT', volumes='77', effects='NN', speed=10)
        pyxel.sound(1).set(notes='G2G2', tones='NN', volumes='33', effects='NN', speed=10)

    # 更新処理：アイテムの次の表示を決める
    def update(self):

        if self.mode == MENU_MODE:
            if pyxel.btn(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.mode = GAME_MODE
            
            return

        if self.check_gameover():
            return

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()


        # クリアした場合は、画面を初期化する
        if self.check_clear():
            self.hitStatus = '--'
            self.init_kusi()
            self.init_dango()

        # 次の表示　くし
        self.update_kusi()

        # 次の表示　団子＆シャボン玉ほか
        self.update_dango()

        # ヒットしているかチェック
        self.check_hit()

        # チェック後の表示　団子＆シャボン玉ほか
        self.update_dango2()
        
        # LIFEが無くなるとゲームオーバー
        if self.life < 0:
            self.gameover_flag = True

    # 次の表示 くし
    def update_kusi(self):
        self.kusi_x = pyxel.mouse_x

    # 次の表示 団子
    def update_dango(self):
        for i in range(0,len(self.maru)):
            self.maru[i].setMaruX(self.maru[i].getMaruX() + self.maru[i].getVxs() * self.speed)
            self.maru[i].setMaruY(self.maru[i].getMaruY() + self.maru[i].getVys() * self.speed)

    # ヒットしているかチェック
    def check_hit(self):
        for i in range(0,len(self.maru)):
            if self.maru[i].getHit() == False:
                hit = self.hit(
                        self.maru[i].getMaruX(),
                        self.maru[i].getMaruY(),
                        MARU_MAP[self.maru[i].getType()][2],
                        self.kusi_x,
                        self.kusi_y,
                        KUSI_W)
                self.maru[i].setHit(hit)
                # ヒット状態：イメージマップ表示を選択
                if self.maru[i].getType() == 0 or self.maru[i].getType() == 1:
                    if hit:
                        pyxel.play(0,0)
                        if self.hitStatus[0] == '-':
                            self.hitStatus = str(self.maru[i].getType()) + self.hitStatus[1]
                        else:
                            if self.hitStatus[1] == '-':
                                self.hitStatus = self.hitStatus[0] + str(self.maru[i].getType())

                # スコア計算
                self.calcScore(i)

    # 画面クリアしているかチェック
    def check_clear(self):
        return (self.hitStatus == '00' or self.hitStatus == '01' or self.hitStatus == '10' or self.hitStatus == '11')

    # ゲームオーバーかチェック
    def check_gameover(self):
        self.life < 0
        return

    # チェック後の表示　団子＆シャボン玉ほか
    def update_dango2(self):
        for i in range(0,len(self.maru)):
            # ヒットした場合は、再度上から降ってくるように
            if self.maru[i].getHit():
                self.maru[i].setMaruY(self.maru[i].getMaruY() + SCREEN_H)
                self.maru[i].setHit(False)

            # ボールが下まで落ちた時の処理
            if self.maru[i].getMaruY() >= SCREEN_H:
                self.maru[i].setMaruX(pyxel.rndi(0,199))
                self.maru[i].setMaruY(0)
                self.angle = pyxel.rndi(30,150)
                self.maru[i].setVxs(pyxel.cos(self.angle))
                self.maru[i].setVys(pyxel.sin(self.angle))
                continue

            # ボールが左右の壁に当たった時の処理
            if (self.maru[i].getMaruX() >= SCREEN_W and self.maru[i].getVxs() > 0) or (self.maru[i].getMaruX() <= 0 and self.maru[i].getVxs() < 0):
                self.maru[i].setVxs(self.maru[i].getVxs() * -1)

        # スコアが基準を超えていたらボールを増やす
        if self.score - len(self.maru) * 50 > 0:
            type = pyxel.rndi(0,3)
            self.maru.append(
                Maru(type,
                     pyxel.rndi(0,200), 
                     DANGO1_START_Y, 
                     MARU_MAP[type][2], 
                     MARU_MAP[type][3], 
                     pyxel.cos(pyxel.rndi(30,150)), 
                     pyxel.sin(pyxel.rndi(30,150)),
                     False, 
                     type)
            )

    # 団子とくしがヒットするかどうかを判定する
    def hit(self,dangoX,dangoY,dangoW,kusiX,kusiY,kusiW):
        hitX = (dangoX < kusiX < dangoX + dangoW - kusiW)
        hitY = (dangoY + dangoW - HITY_IN > kusiY)
        return (hitX and hitY)

    def calcScore(self, i):
        # みたらし団子＋10点
        if self.maru[i].getType() == 0:
            if self.maru[i].getHit():
                self.score += 10
        # 黒ゴマ団子＋20点
        if self.maru[i].getType() == 1:
            if self.maru[i].getHit():
                self.score += 20
        # シャボン玉-10点
        if self.maru[i].getType() == 2:
            if self.maru[i].getHit():
                self.score += -10                   
        # ふうせん -LIFE
        if self.maru[i].getType() == 3:
            if self.maru[i].getHit():
                self.life += -1

    # 描画処理
    def draw(self):
        if self.mode == MENU_MODE: 
            pyxel.text(40, 15, "DANGO GAME", 10)
            pyxel.text(30, 35, " MITARASHI +10点", 13)
            pyxel.blt(10,30,
                      IMAGE_MAP,
                      MARU_MAP[self.maru[0].getType()][0],
                      MARU_MAP[self.maru[0].getType()][1],
                      MARU_MAP[self.maru[0].getType()][2],
                      #行末の０は透過色
                      MARU_MAP[self.maru[0].getType()][3],0)
            pyxel.text(30, 55, " KUROGOMA +20点", 13)
            pyxel.blt(10,50,
                      IMAGE_MAP,
                      MARU_MAP[self.maru[1].getType()][0],
                      MARU_MAP[self.maru[1].getType()][1],
                      MARU_MAP[self.maru[1].getType()][2],
                      #行末の０は透過色
                      MARU_MAP[self.maru[1].getType()][3],0)
            pyxel.text(30, 75, " MIZUTAMA -10点", 13)
            pyxel.blt(10,70,
                      IMAGE_MAP,
                      MARU_MAP[self.maru[2].getType()][0],
                      MARU_MAP[self.maru[2].getType()][1],
                      MARU_MAP[self.maru[2].getType()][2],
                      #行末の０は透過色
                      MARU_MAP[self.maru[2].getType()][3],0)
            pyxel.text(30, 95, " HUSEN -LIFE", 13)
            pyxel.blt(10,90,
                      IMAGE_MAP,
                      MARU_MAP[self.maru[3].getType()][0],
                      MARU_MAP[self.maru[3].getType()][1],
                      MARU_MAP[self.maru[3].getType()][2],
                      #行末の０は透過色
                      MARU_MAP[self.maru[3].getType()][3],0)
            pyxel.text(52, 120, "Enter to Start", 12)
            pyxel.text(52, 130, "Escape to Exit", 9)

            return

        if self.gameover_flag:
            pyxel.text(80,100,"GAME OVER!!!",7)
            return

        pyxel.cls(0)
        # スコア表示   
        pyxel.text(0,0,"SCORE: "+str(self.score),7)
        pyxel.text(0,10,"LIFE: "+str(self.life),7)
        pyxel.text(0,20,"DONE: "+str(self.check_clear()),7)
        pyxel.text(0,30,"STATUS: "+str(self.hitStatus),7)

        # くし表示
        self.draw_kusi()

        # 団子表示
        self.draw_dango()

    # くし表示
    def draw_kusi(self):
        pyxel.blt(self.kusi_x,
                  self.kusi_y,
                  IMAGE_MAP,
                  KUSI_MAP[self.hitStatus][0], 
                  KUSI_MAP[self.hitStatus][1],
                  KUSI_MAP[self.hitStatus][2],
                  KUSI_MAP[self.hitStatus][3],
                )

    # 団子表示
    def draw_dango(self):
        for i in range(0,len(self.maru)):
            pyxel.blt(self.maru[i].getMaruX(),
                      self.maru[i].getMaruY(),
                      IMAGE_MAP,
                      MARU_MAP[self.maru[i].getType()][0],
                      MARU_MAP[self.maru[i].getType()][1],
                      MARU_MAP[self.maru[i].getType()][2],
                      #行末の０は透過色
                      MARU_MAP[self.maru[i].getType()][3],0)

App()