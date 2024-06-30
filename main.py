#main.py一定要在“Python大作业”文件夹下运行！
import pygame
import sys
import time
from settings import *

from sprites import Ball, GamePlatform, AirWall, Heart, Platform, Trampoline, Spike, Cannon, Bullet

# 初始化Pygame
pygame.init()

# 屏幕尺寸
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("心球奇旅")

# 加载图像资源
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
blue_ball_image = pygame.image.load(BLUE_BALL_IMAGE_PATH)
red_ball_image = pygame.image.load(RED_BALL_IMAGE_PATH)
heart_image = pygame.image.load(HEART_IMAGE_PATH)
platform_image = pygame.image.load(PLATFORM_IMAGE_PATH)
trampoline_image = pygame.image.load(TRAMPOLINE_IMAGE_PATH)
spike_image = pygame.image.load(SPIKE_IMAGE_PATH)
cannon_image = pygame.image.load(CANNON_IMAGE_PATH)
bullet_image = pygame.image.load(BULLET_IMAGE_PATH)
platform_image = pygame.transform.scale(platform_image, (100, 20))  # 根据需要调整平台大小
replay_button_image = pygame.image.load(REPLAY_BUTTON_IMAGE_PATH)
replay_button_image = pygame.transform.scale(replay_button_image, (50, 50))  # 调整大小
next_button_image = pygame.image.load(NEXT_BUTTON_IMAGE_PATH)
next_button_image = pygame.transform.scale(next_button_image, (50, 50))  # 调整大小

# 调整图像的尺寸
blue_ball_image = pygame.transform.scale(blue_ball_image, (66, 66))
red_ball_image = pygame.transform.scale(red_ball_image, (66, 66))
heart_image = pygame.transform.scale(heart_image, (32, 32))
trampoline_image = pygame.transform.scale(trampoline_image, (66, 30))
spike_image = pygame.transform.scale(spike_image, (50, 50))
cannon_image = pygame.transform.scale(cannon_image, (50, 50))
bullet_image = pygame.transform.scale(bullet_image, (20, 20))

# 设置字体
font = pygame.font.SysFont(None, 36)

# 加载声音文件
jump_sound = pygame.mixer.Sound('src/跳跃.wav')
trampoline_jump_sound = pygame.mixer.Sound('src/蹦床跳跃.wav')
death_sound = pygame.mixer.Sound('src/死亡音效.wav')
heart_sound = pygame.mixer.Sound('src/红心.wav')  # 加载红心音效

# 背景音乐文件路径
LEVEL_MUSIC = {
    1: 'src/nop.mp3',
    2: 'src/butterfly.mp3',
    3: 'src/lovestory.mp3'
}

# 创建精灵组
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
hearts = pygame.sprite.Group()
flying_hearts = pygame.sprite.Group()
trampolines = pygame.sprite.Group()
spikes = pygame.sprite.Group()
bullets = pygame.sprite.Group()
cannons = pygame.sprite.Group()

# 创建地面平台
ground_height = 1  # 设置为1像素高
ground = Platform(0, SCREEN_HEIGHT - 35, SCREEN_WIDTH, ground_height)
platforms.add(ground)
all_sprites.add(ground)

# 创建左右空气墙
left_wall = AirWall(0, 0, 35, SCREEN_HEIGHT)
right_wall = AirWall(SCREEN_WIDTH - 35, 0, 35, SCREEN_HEIGHT)
platforms.add(left_wall, right_wall)
all_sprites.add(left_wall, right_wall)

# 当前关卡
current_level = 1


def load_level(level): #关卡加载函数，加载平台、爱心、蹦床、尖刺和火炮的位置
    global PLATFORM_POSITIONS, HEART_POSITIONS, TRAMPOLINE_POSITIONS, SPIKE_POSITIONS, CANNON_POSITIONS
    if level in LEVEL_CONFIG:
        config = LEVEL_CONFIG[level]
        PLATFORM_POSITIONS = config["platforms"]
        HEART_POSITIONS = config["hearts"]
        TRAMPOLINE_POSITIONS = config["trampolines"]
        SPIKE_POSITIONS = config["spikes"]
        CANNON_POSITIONS = config["cannons"]
    
    # 根据关卡播放背景音乐
    if level in LEVEL_MUSIC:
        pygame.mixer.music.load(LEVEL_MUSIC[level])
        pygame.mixer.music.play(-1)  # 循环播放

def reset_level(): #重置关卡函数
    global all_sprites, platforms, hearts, flying_hearts, trampolines, spikes, cannons, bullets, ball1, ball2, level_completed
    all_sprites.empty()
    platforms.empty()
    hearts.empty()
    flying_hearts.empty()
    trampolines.empty()
    spikes.empty()
    bullets.empty()
    cannons.empty()
    
    # 重新创建地面平台和空气墙
    platforms.add(ground)
    all_sprites.add(ground)
    platforms.add(left_wall, right_wall)
    all_sprites.add(left_wall, right_wall)

    # 重新创建小球
    ball1 = Ball(357, SCREEN_HEIGHT - 35 - 66, blue_ball_image, jump_sound)
    ball2 = Ball(648, SCREEN_HEIGHT - 35 - 66, red_ball_image, jump_sound)
    all_sprites.add(ball1, ball2)

    # 重新创建平台和红心
    for pos in PLATFORM_POSITIONS:
        platform = GamePlatform(pos[0], pos[1], platform_image)
        platforms.add(platform)
        all_sprites.add(platform)

    for pos in HEART_POSITIONS:
        heart = Heart(pos[0], pos[1], heart_image)
        hearts.add(heart)
        all_sprites.add(heart)

    # 重新创建蹦床
    for pos in TRAMPOLINE_POSITIONS:
        trampoline = Trampoline(pos[0], pos[1], trampoline_image, trampoline_jump_sound)
        trampolines.add(trampoline)
        all_sprites.add(trampoline)

    # 重新创建尖刺
    for pos in SPIKE_POSITIONS:
        spike = Spike(pos[0], pos[1], spike_image)
        spikes.add(spike)
        all_sprites.add(spike)

    # 重新创建火炮
    for pos in CANNON_POSITIONS:
        cannon = Cannon(pos[0], pos[1], cannon_image, bullet_image)
        cannons.add(cannon)
        all_sprites.add(cannon)

    level_completed = False

def next_level(): #下一关函数
    global current_level
    current_level += 1
    load_level(current_level)
    reset_level()

# 加载初始关卡
load_level(current_level)
reset_level()

def restart_level(): # 重新开始关卡函数
    time.sleep(2)
    reset_level()

def handle_death(): #处理死亡函数
    death_sound.play()
    restart_level()

# 游戏主循环
clock = pygame.time.Clock()
running = True
level_completed = False  # 关卡完成标志

replay_button_rect = replay_button_image.get_rect()
replay_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

next_button_rect = next_button_image.get_rect()
next_button_rect.center = (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 50)

while running:
    for event in pygame.event.get(): #处理用户输入
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #按下时移动
            if event.key == pygame.K_a:
                ball1.move("left")
            if event.key == pygame.K_d:
                ball1.move("right")
            if event.key == pygame.K_w:
                ball1.jump()
            if event.key == pygame.K_LEFT:
                ball2.move("left")
            if event.key == pygame.K_RIGHT:
                ball2.move("right")
            if event.key == pygame.K_UP:
                ball2.jump()
        elif event.type == pygame.KEYUP: #按键抬起停止
            if event.key == pygame.K_a:
                ball1.stop_move("left")
            if event.key == pygame.K_d:
                ball1.stop_move("right")
            if event.key == pygame.K_LEFT:
                ball2.stop_move("left")
            if event.key == pygame.K_RIGHT:
                ball2.stop_move("right")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #鼠标事件
            mouse_pos = pygame.mouse.get_pos()
            if replay_button_rect.collidepoint(mouse_pos):
                reset_level()
            elif next_button_rect.collidepoint(mouse_pos):
                next_level() 

    # 更新所有精灵
    all_sprites.update()

    # 检测火炮是否需要发射炮弹
    for cannon in cannons:
        bullet = cannon.shoot()
        if bullet:
            bullets.add(bullet)
            all_sprites.add(bullet)

    # 检测小球和平台之间的碰撞
    for ball in [ball1, ball2]:
        hits = pygame.sprite.spritecollide(ball, platforms, False)
        for hit in hits:
            if ball.change_y > 0:  # 小球正在下落
                if ball.rect.bottom <= hit.rect.top + ball.change_y:
                    ball.change_y = 0 #落地y速度为0
                    ball.rect.bottom = hit.rect.top
                    ball.on_ground = True
            elif ball.change_y < 0:  # 小球正在上升
                if ball.rect.top >= hit.rect.bottom + ball.change_y:
                    ball.change_y = abs(ball.change_y)  # 触顶反弹y速度

    # 检测小球和爱心之间的碰撞
    for ball in [ball1, ball2]:
        heart_hits = pygame.sprite.spritecollide(ball, hearts, False)
        for heart in heart_hits:
            if not heart.flying:
                heart.flying = True
                hearts.remove(heart)
                flying_hearts.add(heart)
                all_sprites.add(heart)
                heart_sound.play()  # 播放红心音效

    # 更新飞行中的爱心
    for heart in flying_hearts:
        if heart.update():
            flying_hearts.remove(heart)

    # 检测小球和蹦床之间的碰撞
    for ball in [ball1, ball2]:
        trampoline_hits = pygame.sprite.spritecollide(ball, trampolines, False)
        for trampoline in trampoline_hits:
            if ball.change_y > 0:  # 小球正在下落
                if ball.rect.bottom <= trampoline.rect.top + ball.change_y:
                    trampoline.bounce(ball)

    # 检测小球和尖刺之间的碰撞
    for ball in [ball1, ball2]:
        spike_hits = pygame.sprite.spritecollide(ball, spikes, False)
        if spike_hits:
            handle_death()

    # 检测小球和炮弹之间的碰撞
    for ball in [ball1, ball2]:
        bullet_hits = pygame.sprite.spritecollide(ball, bullets, False)
        if bullet_hits:
            handle_death()

    #检查通关条件是否达成
    # 检查是否所有爱心都被收集
    if len(hearts) == 0:
        # 检查两个小球是否接触
        if pygame.sprite.collide_rect(ball1, ball2):
            level_completed = True

    # 绘制背景图像
    screen.blit(background_image, (0, 0))
    # 绘制所有精灵
    all_sprites.draw(screen)

    if level_completed:
        # 绘制重玩和下一关按钮
        screen.blit(replay_button_image, replay_button_rect)
        screen.blit(next_button_image, next_button_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
