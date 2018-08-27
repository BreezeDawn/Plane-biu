import random
import pygame
import sys
from pygame.locals import *
from Plane import BigEnemy, SmallEnemy, Award, EnemyPlane,HeroPlane
from Biu import Bullet, EnemyBullet


class CreatEnemys(object):
    # 敌机与炸弹随机率分母
    probability = 4000
    def __init__(self, screen, item, font, super):
        """万能类初始化"""
        # 帧率
        self.clock = 100
        # 敌机列表
        self.enemys = []
        # 炸弹列表
        self.awards = []
        # 英雄飞机对象
        self.item = item
        # 字体对象
        self.font = font
        # Boss飞机对象
        self.super = super
        # 窗体对象
        self.screen = screen
        # 初始化的背景图
        self.bg = pygame.image.load("./feiji/background.png")
        # 暂停图
        self.pause = pygame.image.load('./feiji/game_resume_nor.png')
        # 按键字典初始化
        self.move = {K_UP: 0, K_DOWN: 0, K_LEFT: 0, K_RIGHT: 0, K_w: 0, K_s: 0, K_a: 0, K_d: 0, K_SPACE: 0,K_e:0}

    def create(self):
        """随机创建小飞机/中飞机/大飞机"""
        # 从1-4000中随机,当数字与规定吻合,创建对应飞机
        num = random.randint(1, CreatEnemys.probability)
        # 1/100的几率创建小飞机
        if (num in range(0, 20)) or (num in range(1111, 1131)):
            enemy = SmallEnemy(self.screen, self.item)
            self.enemys.append(enemy)
        # 1/1000的几率创建中飞机
        if num in range(300, 304):
            enemy = EnemyPlane(self.screen, self.item)
            self.enemys.append(enemy)
        # 1/4000的几率创建大飞机
        if num == 500:
            enemy = BigEnemy(self.screen, self.item)
            self.enemys.append(enemy)
        # 遍历每架敌机
        for enemy in self.enemys:
            # 判断敌机是否越界,越界从敌机列表移除
            if enemy.is_out() == '1':
                self.enemys.remove(enemy)
            # 判断敌机是否被打爆,爆炸从敌机列表移除
            if enemy.is_boom() == '1':
                self.enemys.remove(enemy)
                # 敌机爆炸音效
                boom = pygame.mixer.Sound("./feiji/sound/enemyboom.wav")
                boom.play()
                # 分数增加,增加值为敌机代表的分值
                self.item.kill_goal(enemy.goal)
            # 判断敌机是否打爆英雄飞机,爆炸调用英雄飞机爆炸方法,初始化游戏数据
            if enemy.kill_hero() == '1':
                self.item.boom(self.enemys, self.font, self.move)
                # 英雄飞机被打爆的音效
                gameover = pygame.mixer.Sound("./feiji/sound/game_over.wav")
                gameover.play()
                break
            # 遍历到的敌机移动并显示
            enemy.move()
            enemy.display()

    def award(self, bomb):
        """炸弹"""
        # 炸弹的随机创建
        num = random.randint(1, CreatEnemys.probability)
        # 3/4000的几率出现炸弹,出现时添加进炸弹列表以遍历显示
        if num in range(600, 603):
            award = Award(self.screen, self.item)
            self.awards.append(award)
        # 遍历炸弹列表
        for award in self.awards:
            # 如果炸弹列表中的这个炸弹被英雄飞机得到,就从炸弹列表中移除,英雄飞机持有炸弹数加一
            if award.is_get() == '1':
                self.awards.remove(award)
                self.item.awards += 1
                # 得到炸弹的音效
                getaward = pygame.mixer.Sound("./feiji/sound/get_award.wav")
                getaward.play()
            # 遍历的炸弹自然下落并显示
            award.move()
            award.display()
        # 左下角绑定炸弹图标
        self.screen.blit(bomb, (0, 640))
        # 显示英雄飞机持有炸弹数量
        awa = self.font.render('×'+str(self.item.awards), True, (0, 0, 0))
        self.screen.blit(awa, (65, 645))


    def kill_judge(self, item):
        """Boss的击杀/被击杀判断"""
        # 判断Boss是否击杀英雄飞机,如果击杀,调用英雄飞机爆炸方法
        if item.kill_hero(self.item, self.font) == '1':
            self.item.boom(self.enemys, self.font, self.move)
            gameover = pygame.mixer.Sound("./feiji/sound/game_over.wav")
            gameover.play()
        # 如果Boss被击杀,敌机与炸弹随机率初始化,调用英雄飞机爆炸方法,并传入通关标记
        if item.is_boom(self.item) == '1':
            CreatEnemys.probability = 4000
            end = '1'
            self.item.boom(self.enemys, self.font, self.move, end)

    def diff_judge(self):
        """游戏难度调整"""
        # 当分数在25000以下时随机创建敌机,25000以上进入Boss关卡
        if self.item.goal < 25000:
            self.create()
        else:
            # Boss的显示与击杀/被击杀判断
            self.super.display()
            self.kill_judge(self.super)
        # 分数3000以下时的背景,英雄飞机图英雄飞机子弹和敌机子弹的图标修改
        if self.item.goal < 3000 and self.item.diff == 0:
            self.bg = pygame.image.load("./feiji/background.png")
            self.item.image = pygame.image.load("./feiji/hero1.png")
            Bullet.image = pygame.image.load("./feiji/bullet.png")
            EnemyBullet.image = pygame.image.load("./feiji/bullet1.png")
            self.item.diff = 1
        # 分数3000以上6000以下时的帧率,背景,英雄飞机图英雄飞机子弹和敌机子弹的图标修改
        # 以及敌机移速,英雄飞机移速,敌机子弹移速,敌机子弹随机率,敌机创建随机率,的调整
        # 当英雄飞机标记为0时才进入判断
        if self.item.clock == 0:
            if 6000 > self.item.goal >= 3000 and self.item.diff == 1:
                EnemyPlane.y_move = 1
                HeroPlane.move = 3
                EnemyBullet.y_move = 2
                EnemyPlane.probability = 300
                CreatEnemys.probability = 4000
                Bullet.image = pygame.image.load("./feiji/bullet4.png")
                EnemyBullet.image = pygame.image.load("./feiji/bullet6.png")
                self.bg = pygame.image.load("./feiji/beijing1.jpg")
                self.clock = 110
                self.item.diff = 2
        # 分数6000以上13000以下时的帧率,背景,英雄飞机图英雄飞机子弹和敌机子弹的图标修改
        # 以及敌机移速,英雄飞机移速,敌机子弹移速,敌机子弹随机率,敌机创建随机率,的调整
            elif 13000 > self.item.goal >= 6000 and self.item.diff == 2:
                EnemyPlane.y_move = 2
                HeroPlane.move = 4
                EnemyBullet.y_move = 3
                EnemyPlane.probability = 250
                CreatEnemys.probability = 3000
                Bullet.image = pygame.image.load("./feiji/bullet5.png")
                EnemyBullet.image = pygame.image.load("./feiji/bullet7.png")
                self.item.image = pygame.image.load("./feiji/jinhua1.png")
                self.bg = pygame.image.load("./feiji/beijing3.png")
                self.clock = 130
                self.item.diff = 3
            # 分数13000以上17000以下时的帧率,背景,英雄飞机图英雄飞机子弹和敌机子弹的图标修改
            # 以及敌机移速,英雄飞机移速,敌机子弹移速,敌机子弹随机率,敌机创建随机率,的调整
            elif 17000 > self.item.goal >= 13000 and self.item.diff == 3:
                EnemyPlane.y_move = 3
                HeroPlane.move = 5
                EnemyBullet.y_move = 4
                EnemyPlane.probability = 200
                CreatEnemys.probability = 2500
                Bullet.image = pygame.image.load("./feiji/bullet3.png")
                EnemyBullet.image = pygame.image.load("./feiji/bullet9.png")
                self.item.image = pygame.image.load("./feiji/jinhua2.png")
                self.bg = pygame.image.load("./feiji/beijing2.png")
                self.clock = 150
                self.item.diff = 4
            # 分数17000以上25000以下时的帧率,背景,英雄飞机图英雄飞机子弹和敌机子弹的图标修改
            # 以及敌机移速,英雄飞机移速,敌机子弹移速,敌机子弹随机率,敌机创建随机率,的调整
            elif 25000 > self.item.goal >= 17000 and self.item.diff == 4:
                EnemyPlane.y_move = 4
                HeroPlane.move = 6
                EnemyBullet.y_move = 5
                EnemyPlane.probability = 500
                CreatEnemys.probability = 2000
                Bullet.image = pygame.image.load("./feiji/bullet11.png")
                self.item.image = pygame.image.load("./feiji/jinhua3.png")
                self.bg = pygame.image.load("./feiji/beijing4.png")
                self.clock = 190
                self.item.diff = 5
                # 修改英雄飞机标记,不再进行分数判断
                self.item.clock = 1

    def key_judge(self):
        """键盘按键判断"""
        # 炸弹使用音效
        C = pygame.mixer.Sound("./feiji/sound/C.wav")
        # 子弹发射音效
        biu = pygame.mixer.Sound("./feiji/sound/bullet.wav")
        # 暂停键的图标绑定
        self.screen.blit(self.pause, (435, 650))
        # 不断获取按键状态
        for event in pygame.event.get():
            # 当按键ESC时推出
            if event.type == QUIT:
                sys.exit()
            # 如果有按键按下
            if event.type == KEYDOWN:
                # 判断是否在按键字典中,若在,修改该按键标记
                if event.key in self.move.keys():
                    self.move[event.key] = 1
                # 当按键为C,调用英雄飞机使用炸弹的方法,炸弹使用音效执行
                elif event.key == K_c:
                    C.play()
                    self.item.use_award(self.enemys, self.super)
            # 如果有按键松开
            elif event.type == KEYUP:
                # 判断是否在按键字典中,若在,修改该按键标记
                if event.key in self.move.keys():
                    self.move[event.key] = 0
            # 鼠标点击暂停键的判定,修改暂停图标和暂停键标记,进入暂停循环
            x, y = pygame.mouse.get_pos()
            if x in range(435, 475) and y in range(650, 690):
                if event.type == MOUSEBUTTONDOWN:
                    self.pause = pygame.image.load('./feiji/game_resume_nor.png')
                    self.move[K_e] = 1
        # 根据标记调用飞机的上/下/左/右/发射
        if self.move[K_UP] == 1 or self.move[K_w] == 1:
            self.item.move_up()
        if self.move[K_DOWN] == 1 or self.move[K_s] == 1:
            self.item.move_down()
        if self.move[K_LEFT] == 1 or self.move[K_a] == 1:
            self.item.move_left()
        if self.move[K_RIGHT] == 1 or self.move[K_d] == 1:
            self.item.move_right()
        # 如果是发射键,执行子弹发射音效,调用英雄发射子弹方法
        # 并将发射键标记改回,避免发射不间断,实现效果:一次发射键发射一次
        if self.move[K_SPACE] == 1:
            biu.play()
            self.item.biubiu()
            self.move[K_SPACE] = 0

    def pause_judge(self):
        """暂停键的判断"""

        # 当暂停键被按下时触发,游戏主循环停止,进入暂停循环,直到暂停键被再次按下
        while self.move[K_e]:
            # 将暂停图标修改为被按下的图标并绑定
            self.pause = pygame.image.load('./feiji/game_pause_nor.png')
            self.screen.blit(self.pause, (435, 650))
            # 游戏界面不断刷新,防止游戏崩溃
            pygame.display.update()
            # 键盘按键判断
            for event in pygame.event.get():
                # 点右上角退出程序
                if event.type == QUIT:
                    sys.exit()
                # 当有按键被按下
                if event.type == KEYDOWN:
                    # 如果是暂停键,修改暂停图标,并遍历所有按键进行初始化(当然包括暂停键),避免飞机失控
                    if event.key is K_e:
                        self.pause = pygame.image.load('./feiji/game_resume_nor.png')
                        for k in self.move.keys():
                            self.move[k] = 0
                # 鼠标点击暂停键的判定,修改暂停图标,并遍历所有按键进行初始化(当然包括暂停键),避免飞机失控
                x, y = pygame.mouse.get_pos()
                if x in range(435, 475) and y in range(650, 690):
                    if event.type == MOUSEBUTTONDOWN:
                        self.pause = pygame.image.load('./feiji/game_resume_nor.png')
                        for k in self.move.keys():
                            self.move[k] = 0

    def game_begin(self,screen):
        """游戏开始界面"""
        # 不断循环,直到点击开始或退出,当点击开始,返回游戏开始标记
        while True:
            # 绑定飞机大战标题/游戏开始图标/退出游戏图标/
            screen.blit(self.bg, (0, 0))
            screen.blit(pygame.image.load('./feiji/name.png'), (90, 180))
            screen.blit(pygame.image.load('./feiji/gamebegin1.png'), (185, 310))
            screen.blit(pygame.image.load('./feiji/gamebegin2.png'), (245, 307))
            screen.blit(pygame.image.load('./feiji/quit_nor.png'), (185, 400))
            # 不断更新主界面,防止游戏崩溃
            pygame.display.update()
            # 键盘按键的判断
            for event in pygame.event.get():
                # 点右上角退出程序
                if event.type == QUIT:
                    sys.exit()
                # 获取鼠标位置与状态
                x, y = pygame.mouse.get_pos()
                # 鼠标放在游戏开始范围,判断鼠标是否按下,按下返回游戏开始标记
                if x in range(185, 291) and y in range(307, 333):
                    if event.type == MOUSEBUTTONDOWN:
                        return 1
                # 鼠标放在退出游戏范围,判断鼠标是否按下,按下退出程序
                if x in range(185, 291) and y in range(400, 425):
                    if event.type == MOUSEBUTTONDOWN:
                        sys.exit()