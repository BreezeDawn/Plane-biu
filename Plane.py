import sys
import time
import random
import pygame

from pygame.locals import *
from Biu import EnemyBullet, Left_Bullet, Right_Bullet, SuperBullet


class Plane(object):
    """飞机父类"""

    def __init__(self, screen):
        """定义父类初始化属性"""
        self.screen = screen
        self.x = 0
        self.y = 0
        self.image = pygame.image.load('./feiji/icon72x72.png')
        self.bullets = []

    def display(self):
        """是个飞机都要有显示"""
        self.screen.blit(self.image, (self.x, self.y))
        self.bullets_display()

    def bullets_display(self):
        """是个飞机都要有子弹"""
        for bullet in self.bullets:
            bullet.move()
            if bullet.is_out() == '1':
                self.bullets.remove(bullet)


class Award(Plane):
    """炸弹类也继承飞机类"""

    def __init__(self, screen, item):
        """初始化炸弹坐标与图标"""
        super().__init__(screen)
        self.y = -50
        self.item = item
        self.x = random.randint(0, 440)
        self.image = pygame.image.load('./feiji/prop_type_1.png')

    def is_get(self):
        """判断是否被英雄飞机得到"""
        xboom = self.x + 60
        yboom = self.y + 103
        item = self.item
        x_list = [x for x in range(self.x, xboom)]
        for x in x_list:
            if (x in range(item.x, item.x + 90)) and (yboom - 10 in range(item.y, item.y + 100)):
                if self.item.awards < 99:
                    return '1'

    def display(self):
        """显示"""
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        """自然下落"""
        self.y += 3

    def is_out(self):
        """判断下落是否越界"""
        if self.y > 700:
            return '1'
        else:
            return '0'


class HeroPlane(Plane):
    """英雄飞机"""
    # 移速初始化为3
    move = 3

    def __init__(self, screen):
        """英雄飞机初始化"""
        super().__init__(screen)
        self.image = pygame.image.load('./feiji/hero1.png')
        self.award = pygame.image.load('./feiji/award.png')
        self.x = 190
        self.y = 575
        self.goal = 0
        self.diff = 0
        self.clock = 0
        self.awards = 1

    def biubiu(self):
        """发射子弹时发射两发,因为是双发飞机,并把子弹添加进子弹列表"""
        l_bullet = Left_Bullet(self.x, self.y, self.screen)
        r_bullet = Right_Bullet(self.x, self.y, self.screen)
        self.bullets.append(l_bullet)
        self.bullets.append(r_bullet)

    def use_award(self, items, super):
        # 判断是否使用炸弹
        # 英雄飞机持有炸弹数为0时直接返回
        if self.awards == 0:
            return
        # 持有量为0时且分数在25000以下时执行,当前屏幕所有敌机爆炸
        if self.goal < 25000:
            # 英雄飞机子弹列表清空
            self.bullets.clear()
            # 遍历敌机列表,使每个敌机爆炸
            for item in items:
                # 敌机爆炸过程瞬间显示
                self.screen.blit(item.boom1, (item.x, item.y - 10))
                pygame.display.update()
                time.sleep(0.01)
                self.screen.blit(item.boom2, (item.x, item.y - 10))
                pygame.display.update()
                time.sleep(0.02)
                self.screen.blit(item.boom3, (item.x, item.y - 10))
                pygame.display.update()
                time.sleep(0.03)
                # 爆炸一个分数就刷新一次
                self.kill_goal(item.goal)
            # 敌机列表中的敌机全部爆炸,敌机列表清空
            items.clear()
            # 清空后刷新主界面
            pygame.display.update()
            # 持有炸弹数减一
            self.awards -= 1
        # 否则视为Boss关卡,执行Boss掉血
        else:
            # Boss血量扣除且Boss子弹清空,炸弹数减一,加分数,Boss炸一下
            super.boom -= 25
            super.bullets.clear()
            self.awards -= 1
            self.kill_goal(2500)
            self.screen.blit(super.award_image, (super.x, super.y))
            pygame.display.update()
            time.sleep(0.2)

    def kill_goal(self, item):
        """分数加传入的飞机对应的分数值"""
        self.goal += item

    def boom(self, items, font, move, end='0'):
        """英雄飞机爆炸"""
        current_goal = self.goal
        f = open('goal.dat', 'r')
        # 从分数库中读取历史最高分
        r = eval(f.read())
        # 取当前得分与分数库中的最高分中的最大值
        best_goal = max(r, current_goal)
        # 如果最大值是当前分数且不等于历史最高分,写入分数库并显示床子哦啊记录.
        # (如果等于历史最高分不算创造纪录)
        if best_goal == current_goal and r != current_goal:
            f.close()
            f = open('goal.dat', 'w')
            f.write(str(best_goal))
            f.close()
            content = font.render(u'恭喜你创造了新纪录', True, (255, 0, 0))
        # 如果最大值不是当前分数,就什么也不显示
        else:
            f.close()
            content = font.render('', True, (0, 0, 0))
        # 如果通关标记为1,则显示成功通关,否则就什么也不显示
        if end == '1':
            congratulation = font.render(u'恭喜你成功通关!', True, (255, 0, 0))
        else:
            congratulation = font.render(u'', True, (255, 0, 0))
        # 显示出历史最高分和当前分数
        best = font.render(str(best_goal), True, (0, 0, 0))
        current = font.render(str(current_goal), True, (0, 0, 0))
        # 敌机列表清空,英雄飞机子弹清空,显示英雄飞机爆炸图
        items.clear()
        self.bullets.clear()
        self.screen.blit(pygame.image.load("./feiji/hero_blowup_n1.png"), (self.x, self.y))
        pygame.display.update()
        time.sleep(1)
        # 显示游戏结束图/最高分/当前分数/破纪录/通关
        self.screen.blit(pygame.image.load("./feiji/gameover.png"), (0, 0))
        self.screen.blit(best, (200, 270))
        self.screen.blit(current, (200, 420))
        self.screen.blit(content, (50, 310))
        self.screen.blit(congratulation, (100, 100))
        # 显示英雄飞机固定图,小飞机固定图,重新开始和退出游戏图标
        self.screen.blit(pygame.image.load("./feiji/hero1.png"), (190, 550))
        self.screen.blit(pygame.image.load('./feiji/enemy0.png'), (220, 10))
        self.screen.blit(pygame.image.load('./feiji/restart_nor.png'), (100, 350))
        self.screen.blit(pygame.image.load('./feiji/quit_nor.png'), (280, 350))
        pygame.display.update()
        # 结束后跳出主循环,进入判断结束循环
        self.judge(move)

    def judge(self, move):
        """游戏结束界面循环"""
        # 循环标记,为跳出循环设定
        boo = 1
        while boo:
            # 键盘按键判断
            for event in pygame.event.get():
                # 点右上角退出程序
                if event.type == QUIT:
                    sys.exit()
                # 鼠标位置/状态
                x, y = pygame.mouse.get_pos()
                # 如果鼠标位于重新开始范围
                if x in range(100, 220) and y in range(350, 400):
                    # 且鼠标按下,游戏所有数据初始化
                    if event.type == MOUSEBUTTONDOWN:
                        EnemyPlane.y_move = 1
                        HeroPlane.move = 3
                        EnemyBullet.y_move = 2
                        EnemyPlane.probability = 300
                        self.goal = 0
                        self.diff = 0
                        self.clock = 0
                        self.x = 190
                        self.y = 575
                        self.awards = 1
                        boo = 0
                        for k in move.keys():
                            move[k] = 0
                # 如果鼠标位于退出游戏范围,且鼠标按下,程序退出
                elif x in range(280, 400) and y in range(350, 400):
                    if event.type == MOUSEBUTTONDOWN:
                        sys.exit()

    # 上/下/左/右,移速看设定
    def move_up(self):
        if self.y > 90:
            self.y -= HeroPlane.move

    def move_down(self):
        if self.y < 575:
            self.y += HeroPlane.move

    def move_left(self):
        if self.x > 0:
            self.x -= HeroPlane.move

    def move_right(self):
        if self.x < 380:
            self.x += HeroPlane.move


class EnemyPlane(Plane):
    """中等敌机"""
    # 自动移动速度
    y_move = 1
    # 发射子弹随机率分母
    probability = 300

    def __init__(self, screen, item):
        """中等敌机初始化"""
        super().__init__(screen)
        self.x = random.randint(0, 440)
        self.y = -50
        self.image = pygame.image.load('./feiji/enemy1.png')
        self.image2 = pygame.image.load('./feiji/progress3.png')
        self.image2_2 = pygame.image.load('./feiji/progress3-2.png')
        self.image2_3 = ''
        self.boom1 = pygame.image.load('./feiji/enemy1_down1.png')
        self.boom2 = pygame.image.load('./feiji/enemy1_down2.png')
        self.boom3 = pygame.image.load('./feiji/enemy1_down3.png')
        self.xboom = 70
        self.yboom = 90
        # 子弹列表
        self.bullets = []
        # 血量
        self.boom = 4
        # 英雄飞机对象
        self.item = item
        # 对应分值
        self.goal = 200

    def display(self):
        """中等飞机显示和子弹显示"""
        super().display()
        self.screen.blit(self.image2, (self.x, self.y - 10))
        self.bullets_display()

    def biubiu(self):
        """发射子弹"""
        xboom = self.xboom // 2 - 5
        yboom = self.yboom
        bullet = EnemyBullet(self.x + xboom, self.y + yboom, self.screen)
        self.bullets.append(bullet)

    def is_boom(self):
        """飞机是否爆炸"""
        xboom = self.x + self.xboom
        yboom = self.y + self.yboom
        # 遍历英雄飞机子弹列表
        for bullet in self.item.bullets:
            # 如果英雄飞机子弹和自身重合,血量减少,如果血量为0,自身爆炸,分值响应
            if (bullet.x in range(self.x, xboom)) and (bullet.y in range(self.y, yboom)):
                if self.boom == 0:
                    self.item.bullets.remove(bullet)
                    self.screen.blit(self.boom3, (self.x, self.y - 10))
                    pygame.display.update()
                    time.sleep(0.02)
                    return '1'
                elif 0 < self.boom <= 6:
                    self.item.bullets.remove(bullet)
                    self.image2 = self.image2_2
                    self.boom -= 1
                    break
                else:
                    self.item.bullets.remove(bullet)
                    self.image2 = self.image2_3
                    self.boom -= 1
                    break

    def kill_hero(self):
        """碰撞检测"""
        xboom = self.x + self.xboom
        yboom = self.y + self.yboom
        item = self.item
        # 遍历英雄飞机的整体坐标是否和自身整体坐标重合,如果重合返回碰撞标记
        x_list = [x for x in range(self.x, xboom)]
        for x in x_list:
            if (x in range(item.x + 15, item.x + 85)) and (self.y in range(item.y + 10, item.y + 100)):
                return '1'
                # 子弹碰撞检测
        # 遍历英雄飞机的整体坐标是否和自身子弹重合,如果重合返回碰撞标记
        for bullet in self.bullets:
            if (bullet.x in range(item.x + 15, item.x + 85)) and (bullet.y in range(item.y + 10, item.y + 100)):
                return '1'

    def move(self):
        """敌机自动移动"""
        self.y += EnemyPlane.y_move
        # 敌机随机发射子弹,概率随难度变化
        num = random.randint(1, EnemyPlane.probability)
        if num == 50:
            self.biubiu()

    def is_out(self):
        """敌机越界返回越界标记"""
        if self.y > 700:
            return '1'
        else:
            return '0'


class SmallEnemy(EnemyPlane):
    """敌机-小飞机(继承中等飞机)"""

    def __init__(self, screen, item):
        super().__init__(screen, item)
        self.y = -40
        # 血量
        self.boom = 0
        # 图像临界
        self.xboom = 51
        self.yboom = 40
        # 分值
        self.goal = 100
        # 随机出生的x坐标
        self.x = random.randint(0, 410)
        # 小飞机爆炸图/炸弹效果图/血条图
        self.image = pygame.image.load('./feiji/enemy0.png')
        self.image2 = pygame.image.load('./feiji/progress2.png')
        self.boom1 = pygame.image.load('./feiji/enemy0_down1.png')
        self.boom2 = pygame.image.load('./feiji/enemy0_down2.png')
        self.boom3 = pygame.image.load('./feiji/enemy0_down3.png')


class BigEnemy(EnemyPlane):
    """敌机-大飞机(继承中等飞机)"""

    def __init__(self, screen, item):
        super().__init__(screen, item)
        self.y = -250
        # 血量
        self.boom = 12
        # 分值
        self.goal = 300
        # 图像临界
        self.xboom = 165
        self.yboom = 246
        # 随机出生x坐标
        self.x = random.randint(0, 200)
        # 小飞机爆炸图/炸弹效果图/血条图
        self.image = pygame.image.load('./feiji/enemy2.png')
        self.image2 = pygame.image.load('./feiji/progress.png')
        self.image2_2 = pygame.image.load('./feiji/progress-3.png')
        self.image2_3 = pygame.image.load('./feiji/progress-2.png')
        self.boom1 = pygame.image.load('./feiji/enemy2_down3.png')
        self.boom2 = pygame.image.load('./feiji/enemy2_down4.png')
        self.boom3 = pygame.image.load('./feiji/enemy2_down5.png')

    def move(self):
        """敌机自动移动"""
        self.y += 1
        # 敌机随机发射子弹,有它自己的随机数
        num = random.randint(1, 100)
        if num == 50:
            self.biubiu()


class SuperEnemy(Plane):
    """敌机-Boss飞机(继承飞机类)"""

    def __init__(self, screen):
        super().__init__(screen)
        self.y = 20
        # 根据血量调整费劲状态图的标记
        self.biaoji = 0
        # Boss血量
        self.boom = 500
        # Boss图像临界
        self.xboom = 165
        self.yboom = 246
        # Boss爆炸图/Boss被子弹击打动态效果图
        self.image = pygame.image.load('./feiji/enemy2.png')
        self.boom_image2 = pygame.image.load('./feiji/enemy2_down5.png')
        self.award_image = pygame.image.load('./feiji/enemy2_down1.png')
        self.hit = pygame.image.load('./feiji/hit.png')

    def move_left(self):
        """向左移动"""
        self.x -= random.randint(1, 5)

    def move_right(self):
        """向右移动"""
        self.x += random.randint(1, 5)

    def move(self, font):
        """Boos临界坐标随移动更改"""
        xboom = self.xboom // 2 - 5
        yboom = self.yboom
        # 子弹发射概率
        num = random.randint(1, 150)
        # Boss动态血条
        pygame.draw.rect(self.screen, [0, 255, 0], [0, self.y - 10, self.boom, 6], 0)

        # 自动移动Boss飞机
        if self.x <= 0:
            self.oritation = 'right'
        elif self.x >= 480 - 150:
            self.oritation = 'left'

        if self.oritation == 'right':
            self.move_right()
        elif self.oritation == 'left':
            self.move_left()
        # 根据Boss血量判断进入Boss狂暴阶段,发出警告
        if (350 < self.boom < 400) or (250 < self.boom < 300) or (150 < self.boom < 200 or (0 < self.boom < 100)):
            content = font.render('警告! BOSS 暴走了!', True, (255, 0, 0))
            self.screen.blit(content, (50, 270))
            # 调用狂暴阶段的子弹发射,子弹是动态的
            if num == 10:
                self.biu()
        # 没有狂暴时发射普通子弹
        else:
            if num == 10 or num == 20:
                bullet = EnemyBullet(self.x + xboom, self.y + yboom, self.screen)
                self.bullets.append(bullet)

    def kill_hero(self, item, font):
        """判断杀死英雄飞机"""
        # 不断判断的同时自动移动
        self.move(font)
        # 碰撞检测
        xboom = self.x + self.xboom
        yboom = self.y + self.yboom
        # Boss图像整体坐标的推导列表
        x_list = [x for x in range(self.x, xboom)]
        y_list = [x for x in range(self.y, yboom)]
        # 与英雄飞机整体坐标范围进行重合判断
        for y in y_list:
            if (y in range(item.y + 10, item.y + 100)):
                for x in x_list:
                    if (x in range(item.x + 15, item.x + 85)):
                        return '1'
        # 遍历Boss子弹是否杀死英雄飞机,子弹碰撞检测
        for bullet in self.bullets:
            if (bullet.x in range(item.x + 15, item.x + 85)) and (bullet.y in range(item.y + 10, item.y + 100)):
                return '1'

    def biu(self):
        """动态子弹发射"""
        xboom = self.x + self.xboom
        yboom = self.y + self.yboom
        bullet = SuperBullet(self.x, self.y + yboom, self.screen)
        self.bullets.append(bullet)
        bullet = SuperBullet(xboom, self.y + yboom, self.screen)
        self.bullets.append(bullet)

    def is_boom(self, item):
        """根据英雄飞机的子弹碰撞,调整血量下降增加相应分值"""
        xboom = self.x + self.xboom
        yboom = self.y + self.yboom
        for bullet in item.bullets:
            if (bullet.x in range(self.x, xboom)) and (bullet.y in range(self.y, yboom)):
                item.bullets.remove(bullet)
                item.goal += 100
                self.boom -= 1
                # 被击打动态图
                self.screen.blit(self.hit, (self.x, yboom))
        # 根据血量调整自身状态图
        if self.boom <= 400 and self.biaoji == 0:
            self.image = pygame.image.load('./feiji/enemy2_down1.png')
            self.biaoji = 1
            pygame.display.update()
        elif self.boom <= 300 and self.biaoji == 1:
            self.image = pygame.image.load('./feiji/enemy2_down2.png')
            self.biaoji = 2
            pygame.display.update()
        elif self.boom <= 200 and self.biaoji == 2:
            self.image = pygame.image.load('./feiji/enemy2_down3.png')
            self.biaoji = 3
            pygame.display.update()
        elif self.boom <= 100 and self.biaoji == 3:
            self.image = pygame.image.load('./feiji/enemy2_down4.png')
            self.biaoji = 4
            pygame.display.update()
        elif self.boom <= 0:
            self.screen.blit(self.boom_image2, (self.x, self.y))
            pygame.display.update()
            time.sleep(0.5)
            return '1'
