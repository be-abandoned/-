# sprites.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# 小球类
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, image, jump_sound):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0
        self.jump_speed = -12  # 跳跃速度
        self.on_ground = True  # 标记小球是否在地面上
        self.move_left = False
        self.move_right = False #标记移动方向
        self.jump_sound = jump_sound  # 跳跃声音

    def update(self): #更新小球的位置和状态
        self.gravity()
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # 检测是否碰到空气墙
        if self.rect.left <= 35:  # 碰到左空气墙
            self.rect.left = 35
            self.change_x = 0
        elif self.rect.right >= SCREEN_WIDTH - 35:  # 碰到右空气墙
            self.rect.right = SCREEN_WIDTH - 35
            self.change_x = 0

        if self.on_ground:
            if not self.move_left and not self.move_right:
                self.change_x = 0   #确保在在空中能保持水平速度，而地面上时不会“滑步”

    def gravity(self): #模拟重力影响
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.5  # 调整重力加速度以适应新的屏幕尺寸

    def jump(self): #处理跳跃逻辑
        if self.on_ground:
            self.change_y = self.jump_speed
            self.on_ground = False
            self.jump_sound.play()  # 播放跳跃声音

    def move(self, direction): #处理移动逻辑
        if direction == "left":
            self.change_x = -6
            self.move_left = True
            self.move_right = False
        elif direction == "right":
            self.change_x = 6
            self.move_left = False
            self.move_right = True

    def stop_move(self, direction): #停止移动，保证没有按下水平按键时不动
        if direction == "left":
            self.move_left = False
            if self.on_ground and not self.move_right:
                self.change_x = 0
        elif direction == "right":
            self.move_right = False
            if self.on_ground and not self.move_left:
                self.change_x = 0

# 平台类
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # 设置为全透明
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 游戏平台类(地面)
class GamePlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 空气墙类（使用现有的 Platform 类）
class AirWall(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

# 爱心类
class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (46, 46))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flying = False #是否是飞行状态
        self.target_x = 10  
        self.target_y = 10 #飞行目标位置xy

    def update(self): #更新爱心的位置，如果飞行到目标位置则移除
        if self.flying:
            self.rect.x += (self.target_x - self.rect.x) * 0.1
            self.rect.y += (self.target_y - self.rect.y) * 0.1
            if abs(self.rect.x - self.target_x) < 1 and abs(self.rect.y - self.target_y) < 1:
                self.kill()  # 移除飞行中的爱心
                return True  # 表示飞行结束
        return False

# 蹦床类
class Trampoline(pygame.sprite.Sprite):
    def __init__(self, x, y, image, jump_sound):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.jump_sound = jump_sound  # 蹦床跳跃声音

    def bounce(self, ball): #处理小球在蹦床上的反弹效果，并播放跳跃声音
        ball.change_y = -ball.change_y * 1.2  # 反转垂直速度并增加跳跃高度（反弹指数可修改，来调整蹦床的弹性）
        self.jump_sound.play()  # 播放蹦床跳跃声音
# 尖刺类
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 炮弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = 10  # 炮弹的飞行速度

    def update(self): #更新炮弹的位置，如果超出屏幕则移除
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()

# 火炮类
class Cannon(pygame.sprite.Sprite):
    def __init__(self, x, y, image, bullet_image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bullet_image = bullet_image
        self.last_shot_time = pygame.time.get_ticks()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 4000:  # 每4秒发射一枚炮弹（发射频率）
            self.last_shot_time = current_time
            bullet = Bullet(self.rect.centerx - 10, self.rect.bottom, self.bullet_image)  # 向左移动发射位置
            return bullet
        return None