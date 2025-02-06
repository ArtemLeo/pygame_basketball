import sys
import pygame
import random
import os

class Basketball:

    def __init__(self):
        pygame.init()
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h

        # Set window size to 70% of screen size
        self.width = int(self.screen_width * 0.8)
        self.height = int(self.screen_height * 0.8)
        self.size = self.width, self.height

        self.xspeed_init = 10
        self.yspeed_init = 10
        self.max_lives = 5
        self.bat_speed = 30
        self.score = 0
        self.level = 1
        self.bgcolour = 0x2F, 0x4F, 0x4F

        # Load sounds
        self.pong = pygame.mixer.Sound("assets/sounds/otskok-myacha.mp3")
        self.pong.set_volume(10)

        # Load background music
        pygame.mixer.music.load("assets/sounds/background_music.mp3")
        pygame.mixer.music.set_volume(0.5)  # Set volume to 50%

        # Set window title
        pygame.display.set_caption("PyGame Basketball")

    def load_images(self):
        # Load images after setting video mode
        self.start_image = pygame.image.load("assets/images/start_image.png")
        self.start_image = pygame.transform.scale(self.start_image, self.size)
        self.bat = pygame.image.load("assets/images/bat.png").convert()
        self.bat = pygame.transform.scale(self.bat, (self.bat.get_width() * 2, self.bat.get_height()))
        self.ball = pygame.image.load("assets/images/ball.png").convert_alpha()
        self.ball = self.create_circular_surface(self.ball, 35)
        self.brick = pygame.image.load("assets/images/brick.png").convert()

        # Load background image if it exists
        background_path = "assets/images/background_image.png"
        if os.path.exists(background_path):
            self.background = pygame.image.load(background_path).convert()
            self.background = pygame.transform.scale(self.background, self.size)
        else:
            self.background = None

    def draw_text_with_background(self, screen, text, font_size, center_x, center_y):
        """Draw text with a black background."""
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(center_x, center_y))

        # Create a background surface with black color
        background_rect = pygame.Rect(text_rect.left - 5, text_rect.top - 5, text_rect.width + 10, text_rect.height + 10)
        pygame.draw.rect(screen, (0, 0, 0), background_rect)  # Black background

        screen.blit(text_surface, text_rect)

    def draw_ui(self, screen):
        """Draw the UI elements: score, lives, and level."""
        self.draw_text_with_background(screen, f"Score: {self.score}", 50, 100, 30)
        self.draw_text_with_background(screen, f"Lives: {self.lives}", 50, self.width - 100, 30)
        self.draw_text_with_background(screen, f"Level: {self.level}", 50, self.width // 2, 30)

    def reset_game(self):
        """Reset game variables to initial state."""
        self.score = 0
        self.level = 1
        self.lives = self.max_lives
        self.xspeed = self.xspeed_init
        self.yspeed = self.yspeed_init

    def create_circular_surface(self, image, radius):
        """Create a circular surface for the ball."""
        circular_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(circular_surface, (255, 255, 255), (radius, radius), radius)
        image = pygame.transform.scale(image, (radius * 2, radius * 2))
        circular_surface.blit(image, (0, 0), None, pygame.BLEND_RGBA_MULT)
        return circular_surface

    def show_start_image(self, screen):
        """Show the start image for 5 seconds."""
        screen.blit(self.start_image, (0, 0))
        pygame.display.flip()
        pygame.time.wait(5000)

    def show_start_screen(self, screen):
        """Show the start screen with instructions."""
        self.draw_text_with_background(screen, "Press SPACE to START", 80, self.width // 2, self.height // 2)
        pygame.display.flip()

        while True:
            if self.background:
                screen.blit(self.background, (0, 0))
            else:
                screen.fill(self.bgcolour)
            self.draw_text_with_background(screen, "Press SPACE to START", 80, self.width // 2, self.height // 2)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return

    def main(self):
        """Main game loop."""
        screen = pygame.display.set_mode(self.size)
        self.load_images()  # Load images after setting video mode

        # Start playing background music
        pygame.mixer.music.play(-1)  # Loop indefinitely

        self.show_start_image(screen)
        self.show_start_screen(screen)

        batrect = self.bat.get_rect()
        ballrect = self.ball.get_rect()
        wall = Wall(self.brick)
        wall.build_wall(self.width, self.level)

        batrect.midbottom = (self.width / 2, self.height - 20)
        ballrect.center = (self.width / 2, self.height / 2)
        self.xspeed = self.xspeed_init
        self.yspeed = self.yspeed_init
        self.lives = self.max_lives
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 30)
        pygame.mouse.set_visible(0)

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_LEFT:
                        batrect = batrect.move(-self.bat_speed, 0)
                        if batrect.left < 0:
                            batrect.left = 0
                    if event.key == pygame.K_RIGHT:
                        batrect = batrect.move(self.bat_speed, 0)
                        if batrect.right > self.width:
                            batrect.right = self.width

            ballrect = ballrect.move(self.xspeed, self.yspeed)

            if ballrect.left < 0 or ballrect.right > self.width:
                self.xspeed = -self.xspeed
                self.pong.play(0)

            if ballrect.top < 0:
                self.yspeed = -self.yspeed
                self.pong.play(0)

            if ballrect.top > self.height:
                self.lives -= 1
                self.xspeed = self.xspeed_init * random.choice([-1, 1])
                self.yspeed = self.yspeed_init
                ballrect.center = (self.width * random.random(), self.height / 3)
                if self.lives == 0:
                    self.show_game_over(screen)
                    self.reset_game()
                    wall.build_wall(self.width, self.level)
                    ballrect.center = (self.width / 2, self.height / 2)

            index = ballrect.collidelist(wall.brickrect)
            if index != -1:
                if ballrect.centerx > wall.brickrect[index].right or ballrect.centerx < wall.brickrect[index].left:
                    self.xspeed = -self.xspeed
                else:
                    self.yspeed = -self.yspeed
                self.pong.play(0)
                wall.brickrect.pop(index)
                self.score += 10

            if ballrect.colliderect(batrect):
                self.yspeed = -self.yspeed
                self.pong.play(0)

            if not wall.brickrect:
                self.level += 1
                wall.build_wall(self.width, self.level)
                self.xspeed += 1 if self.xspeed > 0 else -1
                self.yspeed += 1 if self.yspeed > 0 else -1
                ballrect.center = (self.width / 2, self.height / 3)

            if self.background:
                screen.blit(self.background, (0, 0))
            else:
                screen.fill(self.bgcolour)
            self.draw_ui(screen)

            for brick in wall.brickrect:
                screen.blit(self.brick, brick)

            screen.blit(self.ball, ballrect)
            screen.blit(self.bat, batrect)
            pygame.display.flip()

    def show_game_over(self, screen):
        """Show the game over screen."""
        self.draw_text_with_background(screen, "Game Over - Press R to RESTART", 80, self.width // 2, self.height // 2)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return

class Wall:

    def __init__(self, brick):
        self.brick = brick
        brickrect = self.brick.get_rect()
        self.bricklength = brickrect.width
        self.brickheight = brickrect.height
        self.brickrect = []

    def build_wall(self, width, level):
        """Build the wall of bricks."""
        self.brickrect = []
        margin = 30
        xpos = margin
        ypos = 60
        brick_rows = 1 + level

        for _ in range(brick_rows * 10):
            if xpos + self.bricklength > width - margin:
                xpos = margin
                ypos += self.brickheight

            rect = self.brick.get_rect().move(xpos, ypos)
            self.brickrect.append(rect)
            xpos += self.bricklength

if __name__ == '__main__':
    br = Basketball()
    br.main()
