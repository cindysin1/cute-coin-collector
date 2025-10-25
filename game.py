import pygame
import random
import sys
import os

# 初始化pygame
pygame.init()
pygame.mixer.init()

# 确保中文常量定义
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)  # 金币颜色
PLAYER_COLOR = (255, 192, 203)  # 可爱粉色角色

# 游戏参数
TIME_LIMIT = 30  # 30秒/局
TARGET_COINS = 20  # 获胜所需金币数
COIN_SPEED = 3  # 金币下落速度
COIN_SPAWN_RATE = 50  # 每多少帧生成一个金币

# 创建屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("可爱形象吃金币")
clock = pygame.time.Clock()

# 确保中文字体（支持中文）
pygame.font.init()
font_options = ["Arial Unicode MS", "PingFang SC", "SimHei"]
def get_font(size):
    for font_name in font_options:
        try:
            return pygame.font.SysFont(font_name, size)
        except:
            continue
    return pygame.font.Font(None, size)

# 资源路径处理
def resource_path(relative_path):
    """获取资源绝对路径（兼容开发环境和打包后）"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 加载资源
class Resources:
    def __init__(self):
        # 加载图像
        self.player_img = self.create_player_img()
        self.coin_img = self.create_coin_img()
        
        # 加载音效
        self.collect_sound = self.load_sound("coin_sound.wav")
        self.bg_music = self.load_music("bg_music.mp3")
        self.win_sound = self.load_sound("win_sound.wav")
        self.lose_sound = self.load_sound("lose_sound.wav")

    def create_player_img(self):
        """创建可爱的圆形角色（可替换为图片）"""
        img = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(img, PLAYER_COLOR, (25, 25), 25)
        # 画眼睛
        pygame.draw.circle(img, BLACK, (18, 20), 5)
        pygame.draw.circle(img, BLACK, (32, 20), 5)
        # 画微笑
        pygame.draw.arc(img, BLACK, (15, 25, 20, 15), 0, 3.14, 2)
        return img

    def create_coin_img(self):
        """创建金币图像（可替换为图片）"""
        img = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(img, YELLOW, (15, 15), 15)
        pygame.draw.circle(img, (255, 255, 0), (15, 15), 10)
        return img

    def load_sound(self, filename):
        try:
            return pygame.mixer.Sound(resource_path(f"assets/sounds/{filename}"))
        except:
            print(f"警告：未找到音效 {filename}，将静音")
            return None

    def load_music(self, filename):
        try:
            pygame.mixer.music.load(resource_path(f"assets/music/{filename}"))
            return True
        except:
            print(f"警告：未找到背景音乐 {filename}，将静音")
            return False

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self, resources):
        super().__init__()
        self.image = resources.player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 8

    def update(self):
        # 键盘控制
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# 金币类
class Coin(pygame.sprite.Sprite):
    def __init__(self, resources):
        super().__init__()
        self.image = resources.coin_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, SCREEN_WIDTH - 50)
        self.rect.y = random.randint(-100, -30)  # 从屏幕上方掉落
        self.speed = random.uniform(COIN_SPEED - 1, COIN_SPEED + 1)

    def update(self):
        self.rect.y += self.speed
        # 超出屏幕底部则删除
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# 游戏主类
class Game:
    def __init__(self):
        self.resources = Resources()
        self.reset_game()
        
        # 启动背景音乐
        if self.resources.bg_music:
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)

    def reset_game(self):
        """重置游戏状态"""
        self.all_sprites = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        
        self.player = Player(self.resources)
        self.all_sprites.add(self.player)
        
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.game_active = True
        self.win = False

    def spawn_coin(self):
        """随机生成金币"""
        if random.randint(0, COIN_SPAWN_RATE) == 0:
            coin = Coin(self.resources)
            self.all_sprites.add(coin)
            self.coins.add(coin)

    def check_collisions(self):
        """检测金币收集"""
        hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for hit in hits:
            self.score += 1
            if self.resources.collect_sound:
                self.resources.collect_sound.play()
            # 检查胜利条件
            if self.score >= TARGET_COINS:
                self.game_active = False
                self.win = True
                if self.resources.win_sound:
                    self.resources.win_sound.play()

    def check_time(self):
        """检查时间限制"""
        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        self.remaining_time = max(0, TIME_LIMIT - elapsed)
        if self.remaining_time <= 0 and self.game_active:
            self.game_active = False
            self.win = False
            if self.resources.lose_sound:
                self.resources.lose_sound.play()

    def draw_ui(self):
        """绘制UI元素"""
        # 分数显示
        score_text = get_font(30).render(f"金币: {self.score}/{TARGET_COINS}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        # 时间显示
        time_text = get_font(30).render(f"时间: {self.remaining_time}s", True, WHITE)
        screen.blit(time_text, (SCREEN_WIDTH - 180, 20))
        
        # 游戏结束界面
        if not self.game_active:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # 半透明黑色遮罩
            screen.blit(overlay, (0, 0))
            
            result_text = "恭喜胜利！" if self.win else f"游戏结束！得分: {self.score}"
            text = get_font(50).render(result_text, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 50))
            
            restart_text = get_font(30).render("按R键重新开始，ESC键退出", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 30))

    def run(self):
        """游戏主循环"""
        running = True
        while running:
            clock.tick(FPS)
            
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if not self.game_active and event.key == pygame.K_r:
                        self.reset_game()

            # 游戏逻辑
            if self.game_active:
                self.all_sprites.update()
                self.spawn_coin()
                self.check_collisions()
                self.check_time()
            else:
                # 游戏结束时停止玩家移动
                self.player.rect.x = self.player.rect.x  # 保持位置不变

            # 绘制
            screen.fill(BLACK)
            self.all_sprites.draw(screen)
            self.draw_ui()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()