import pygame
import os
import sys
import random
pygame.init()
# 实现发射子弹
# Global Constants

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('恐龙小游戏')

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]
REDRUNNING = [pygame.image.load(os.path.join("Assets/Dino", "redDinoRun1.png")),
             pygame.image.load(os.path.join("Assets/Dino", "redDinoRun2.png"))]
REDJUMPING = pygame.image.load(os.path.join("Assets/Dino", "redDinoJump.png"))
REDDUCKING = [pygame.image.load(os.path.join("Assets/Dino", "redDinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "redDinoDuck2.png"))]
BULLET = pygame.image.load(os.path.join("Assets/Other", "Pepper.png"))

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

PEPPER = pygame.image.load(os.path.join("Assets/Other", "Pepper.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 80    # run小恐龙位置
    Y_POS = 310     # run小恐龙位置
    Y_POS_DUCK = 340    # 小恐龙下蹲位置
    JUMP_VEL = 8.5      # 小恐龙

    def __init__(self):
        self.duck_img = DUCKING     # 2 个图片
        self.run_img = RUNNING      # 2 个图片
        self.jump_img = JUMPING     # 1 个图片    # 读入状态图片

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False      # 初始化run状态

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.shoted = 0


    def redDino(self):
        self.duck_img = REDDUCKING
        self.run_img = REDRUNNING  # 2 个图片
        self.jump_img = REDJUMPING  # 1 个图片    # 读入状态图片


    def update(self, userInput, eatpepper):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        if userInput[pygame.K_SPACE] and eatpepper == 2:
            self.duck_img = DUCKING  # 2 个图片
            self.run_img = RUNNING  # 2 个图片
            self.jump_img = JUMPING  # 1 个图片    # 读入状态图片
            self.shoted = 1


    def duck(self):
        self.image = self.duck_img[self.step_index // 5]        # 根据 step_index 来刷新图片，每 5 帧刷新一次
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]         # 根据 step_index 来刷新图片，每 5 帧刷新一次
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

# 创建子弹类
class Bullet():
    def __init__(self,player):
        self.bullet = BULLET
        self.bullet = pygame.transform.scale(self.bullet, (50, 30))
        self.bullet_rect = self.bullet.get_rect()
        self.bullet_rect.x = player.dino_rect.x+20
        self.bullet_rect.y = player.dino_rect.y
        self.step = 10

    def update(self):
        self.bullet_rect.x += self.step
        if self.bullet_rect.x > SCREEN_WIDTH:
            bullets.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.bullet, self.bullet_rect)


# 随机生成云
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

# 随机生成辣椒
class Pepper:
    def __init__(self, image):
        self.image = image
        self.image = pygame.transform.scale(self.image, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = 5000

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            peppers.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)

class littlepepper(Pepper):
    def __init__(self, image):
        super().__init__(image)
        self.rect.y = 200


# 障碍物组
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, peppers
    global eatpepper, redcolor, bullets
    bullets = []
    redcolor = 0
    eatpepper = 0

    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    # 引入字体类型
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    peppers = []
    death_count = 0



    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        # 生成文本信息
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        # 获得并设置文本信息的rect区域坐标
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        # 将准备好的文本信息绘制到主屏幕上
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # 全窗口填充白色
        SCREEN.fill((255, 255, 255))
        # 接收一个按键，按键为 上 或 下
        userInput = pygame.key.get_pressed()
        # 绘制小恐龙
        player.draw(SCREEN)
        # 小恐龙根据接收按键 修改小恐龙的状态    其中状态分为 run jump duck
        player.update(userInput,eatpepper)
        # 随机生成障碍物
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))
        # 如果小恐龙矩形碰撞到障碍物 则死亡

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for b in bullets:
                b.draw(SCREEN)
                b.update()
                if b.bullet_rect.colliderect(obstacle.rect):
                    obstacles.remove(obstacle)
                    bullets.remove(b)
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        # 随机生成小辣椒
        if len(peppers) == 0:
            peppers.append(littlepepper(PEPPER))
        for pepper in peppers:
            pepper.draw(SCREEN)
            pepper.update()
            if player.dino_rect.colliderect(pepper.rect):
                # 碰到辣椒触发事件  吃掉小辣椒
                if(eatpepper < 2):
                    eatpepper += 1
                peppers.remove(pepper)
        if(redcolor==0 and eatpepper == 2):
            print('变红')
            redcolor = 1
            player.redDino()

        if(player.shoted == 1):
            bullets.append(Bullet(player))
            player.shoted = 0
            redcolor = 0
            eatpepper = 0

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        # 填充白色底色
        SCREEN.fill((255, 255, 255))
        # 设置字体类型
        font = pygame.font.Font('freesansbold.ttf', 30)
        # 生成文本信息
        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        # 按下按键调用 main  开始游戏   若游戏中按下 × 则回到开始界面
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    # 在等待开始界面如果按下 ×  则退出游戏
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

menu(death_count=0)