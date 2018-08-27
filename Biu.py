import pygame
import random


class Bullet(object):
    """子弹父类"""
    # 子弹图像/可调整
    image = pygame.image.load('./feiji/bullet.png')
    def __init__(self, x, y, screen):
        """子弹初始化"""
        self.x = x
        self.y = y
        self.screen = screen
        self.image = Bullet.image

    def move(self):
        """自动移动"""
        self.screen.blit(self.image, (self.x, self.y))
        self.y -= 5

    def is_out(self):
        """判断子弹越界"""
        if self.y < 0:
            return '1'
        else:
            return '0'


class EnemyBullet():
    """中等飞机子弹类"""
    # 子弹图像/可调整
    image = pygame.image.load('./feiji/bullet2.png')
    # 子弹移速/可调整
    y_move = 2
    def __init__(self, x, y, screen):
        """中等飞机子弹初始化"""
        # 子弹出现位置根据飞机位置调整
        self.x = x
        self.y = y
        self.screen = screen
        self.image = EnemyBullet.image

    def move(self):
        """子弹自动移动"""
        self.screen.blit(self.image, (self.x, self.y))
        self.y += EnemyBullet.y_move

    def is_out(self):
        """子弹越界返回越界标记"""
        if self.y > 800:
            return '1'
        else:
            return '0'


class SuperBullet(EnemyBullet):
    """Boss飞机动态子弹类"""
    # 子弹图像/可调整
    image = pygame.image.load('./feiji/bullet2.png')
    def __init__(self, x, y, screen):
        """Boss动态子弹初始化"""
        super(SuperBullet, self).__init__(x, y, screen)
        # 控制动态子弹移动规律
        num = random.randint(1, 2)
        if num == 1:
            self.num = 0
        else:
            self.num = 100

    def move(self):
        """动态子弹的移动"""
        # 子弹图像和移速
        self.screen.blit(self.image, (self.x, self.y))
        self.y += 2
        # 动态子弹的移动规则,左/右
        if 50 < self.num <= 100:
            self.x -= 2
            self.num -= 1
            if self.num == 50:
                self.num = 0
        elif 0 <= self.num < 50:
            self.x += 2
            self.num += 1
            if self.num == 50:
                self.num = 100


class Left_Bullet(Bullet):
    """英雄飞机的左发射口的子弹类"""
    def __init__(self, x, y, screen):
        # 子弹初始化
        super().__init__(x, y, screen)
        self.x = x + 7
        self.y = y + 10


class Right_Bullet(Bullet):
    """英雄飞机的右发射口的子弹类"""
    def __init__(self, x, y, screen):
        # 子弹初始化
        super().__init__(x, y, screen)
        self.x = x + 73
        self.y = y + 10
