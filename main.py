"""游戏：飞机大战"""
import os


import pygame
from pygame.locals import *

from Plane import HeroPlane, SuperEnemy
from CreatEnemy import CreatEnemys


def main():
    # 程序当前目录没有积分数据库,则创建积分数据库
    if 'goal.dat' in os.listdir():
        pass
    else:
        f = open('goal.dat', 'w')
        f.write('0')
        f.close()
    # 字体的初始化
    pygame.font.init()
    font = pygame.font.SysFont('SimHei', 44)
    # 创建窗体
    screen = pygame.display.set_mode((480, 700), 0, 32)
    # 定义爆炸效果图
    bomb = pygame.image.load("./feiji/bomb.png")
    # 创建英雄飞机对象
    hero = HeroPlane(screen)
    # 创建Boss飞机对象
    superenemy = SuperEnemy(screen)
    # 创建敌机群对象 - 万能类
    enemys = CreatEnemys(screen, hero, font, superenemy)
    # 帧率控制
    clock = pygame.time.Clock()
    # 音频初始化
    pygame.mixer.init()
    pygame.mixer.music.load("./feiji/sound/98K.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    # 开始界面,由返回值判定开始游戏/结束游戏
    r = enemys.game_begin(screen)
    # 当点击开始游戏,进入循环主体
    while r:
        # 绑定背景图,背景图由万能类控制
        screen.blit(enemys.bg, (0, 0))
        # 绑定得分,分数由英雄飞机类的分数判定方法返回
        goal = font.render(str(hero.goal), True, (0, 0, 0))
        screen.blit(goal, (0, 225))
        # 键盘按键判断放在万能类中
        enemys.key_judge()
        # 游戏难度由万能类判定
        enemys.diff_judge()
        # 显示英雄飞机
        hero.display()
        # 炸弹的显示/得到/使用,也由万能类控制
        enemys.award(bomb)
        # 暂停按键的判断,也由万能类判断
        enemys.pause_judge()
        # 主界面刷新
        pygame.display.update()
        # 帧率控制也在万能类....
        clock.tick(enemys.clock)

if __name__ == '__main__':
    main()
