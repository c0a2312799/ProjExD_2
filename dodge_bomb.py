import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0, -5), 
         pg.K_DOWN:(0, +5), 
         pg.K_LEFT:(-5, 0), 
         pg.K_RIGHT:(+5, 0),
         }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

acs =[a for a in range(1, 11)]
bb_imgs = []
for r in range(1, 11):
    bb_img = pg.Surface((20 * r, 20 * r))
    pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)


#def ensyuu2():
#    avx = vx * bb_accs[min(tmr//500, 9)]
#    bb_img = bb_imgs[min(tmr//500, 9)]


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん, または, 爆弾のRect
    戻り値：真理値タプル（横判定結果, 縦判定結果）
    仮面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # スクリーンの生成
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200  # こうかとんの初期位置を設定
    kk_img2 = pg.transform.rotozoom(pg.image.load("fig/6.png"), 0, 0.9)
    kk_rct2 = kk_img2.get_rect()
    bb_img = pg.Surface((20, 20))  # 空のSurface
    bb_img.set_colorkey((0, 0, 0))  # 円の外側の色を透過させる
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出 
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])  # blitは背景画像貼り付け
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が重なっていたら
            fonto = pg.font.Font(None, 80)
            txt = fonto.render("Game Over", True, (255, 255, 255))
            go = pg.Surface((WIDTH, HEIGHT))
            pg.draw.rect(go, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
            go_rct = go.get_rect()
            go.set_alpha(100)
            screen.blit(go, go_rct)
            screen.blit(txt, [400, 300])
            screen.blit(kk_img2, [710, 300])
            pg.display.update()
            pg.time.wait(5000)
            return 
        

        key_lst = pg.key.get_pressed()  # キー反応するやつ
        sum_mv = [0, 0]  # 横座標, 縦座標
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向
        kk_rct.move_ip(sum_mv)  # こうかとん移動するやつ
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        level = min(tmr // 500, 9)
        avx = vx * acs[level]
        bb_rct.move_ip(avx, vy)
        screen.blit(bb_imgs[level], bb_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1 
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
