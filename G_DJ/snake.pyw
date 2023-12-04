import pygame
from random import randint
import time
import random

# Load multiple step sound files


pygame.init()
window = pygame.display.set_mode((1280, 720))
ouch = pygame.mixer.Sound("eat.wav")
oof=pygame.mixer.Sound("haha.WAV")
levelup = pygame.mixer.Sound("LEVELUP.WAV")
leveldown= pygame.mixer.Sound("leveldown.WAV")
step= [pygame.mixer.Sound(f"STEP_EARTH_0{i}.wav") for i in range(1, 6)]  # Adjust the range based on your filenames


print(pygame.font.get_fonts())

class Player:
    def __init__(self):
        self.x_cord = window.get_width()/2  # współrzędna x
        self.y_cord = window.get_height()/2  # współrzędna y
        self.image = pygame.transform.scale(pygame.image.load("apple.webp"), (100, 120))  # wczytuje grafikę
        self.last_step_time = 0
        self.width = self.image.get_width()  # szerokość
        self.height = self.image.get_height()  # wysokość
        self.speed = 4  # prędkość
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

        self.walk_frames_right = [pygame.transform.scale(pygame.image.load(f"animation/frame_{i}.webp"), (self.width, self.height)) for i in
                            range(1, 12)]
        self.walk_frames_left = [pygame.transform.scale(pygame.transform.flip(pygame.image.load(f"animation/frame_{i}.webp"),True,False) , (self.width, self.height)) for i in
                            range(1, 12)]

        self.walk_index = 0  # Index to keep track of the current frame
        self.animation_speed = 0.07  # Adjust the speed of the animation
        self.last_animation_time = 0

    def tick(self, keys):  # wykonuje się raz na powtórzenie pętli
        if keys[pygame.K_w]:
            self.y_cord -= self.speed

        if keys[pygame.K_a]:
            self.x_cord -= self.speed

        if keys[pygame.K_s]:
            self.y_cord += self.speed

        if keys[pygame.K_d]:
            self.x_cord += self.speed


        # Check if any movement keys are pressed
        if any(keys[key] for key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]):

            current_time = pygame.time.get_ticks()
            # Play the step sound every 500 milliseconds (adjust the interval as needed)
            if current_time - self.last_step_time > 500:
                random.choice(step).play()
                self.last_step_time = current_time

            # Update the walking animation
            if current_time - self.last_animation_time > self.animation_speed * 1000:  # Adjust the interval for animation frames
                self.walk_index = (self.walk_index + 1) % len(self.walk_frames_right)

                # Determine the direction the player is moving
                if keys[pygame.K_a] or keys[pygame.K_s]:  # Moving left
                    self.image = self.walk_frames_left[self.walk_index]
                else:  # Moving right or other directions
                    self.image = self.walk_frames_right[self.walk_index]

                self.last_animation_time = current_time

        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))


class Food:
    def __init__(self):
        self.x_cord = randint(0, 1100)
        self.y_cord = randint(0, 500)
        self.image = pygame.transform.scale(pygame.image.load("bezi.webp"), (100, 320))
        self.width = self.image.get_width()  # szerokość
        self.height = self.image.get_height()  # wysokość
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width/2, self.height)
        self.spawn_time = 0

    def tick(self):
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width/2, self.height)

    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))

class Enemy:
    def __init__(self):
        self.x_cord = randint(0, 1100)
        self.y_cord = randint(0, 500)
        self.image = pygame.transform.scale(pygame.image.load("Kruk.png"), (100, 320))
        self.width = self.image.get_width()  # szerokość
        self.height = self.image.get_height()  # wysokość
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width/2, self.height)
        self.spawn_time = 0


    def tick(self):
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width/2, self.height)

    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))


def main():
    run = True
    player = Player()
    clock = 0
    enemy_spawn_timer = 0
    food_spawn_timer = 0
    score = 0
    unscore= 0
    banknotes = []
    enemies=[]


    played=False
    played_unmisc=False

    background = pygame.transform.scale(pygame.image.load("grass.jpg"), (1280, 720))

    while run:
        clock += pygame.time.Clock().tick(60) / 1000  # maksymalnie 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # jeśli gracz zamknie okienko
                run = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            run=False

        enemy_spawn_timer += clock
        food_spawn_timer += clock
        print(food_spawn_timer)

        if food_spawn_timer >= 1000:
            food_spawn_timer= 0
            banknotes.append(Food())

        if enemy_spawn_timer >= 6000:
            enemy_spawn_timer=0
            enemies.append(Enemy())


        player.tick(keys)
        for banknote in banknotes:
            banknote.tick()

        for enemy in enemies:
            enemy.tick()

        score_icon = pygame.transform.scale(pygame.image.load("bezi_head.png"), (60, 60))
        score_text = pygame.font.Font.render(pygame.font.SysFont('segoeuiemoji', 60), f' {str(score)}', True, (200, 0, 0))

        window.blit(background, (0, 0))  # rysowanie tła
        window.blit(score_text, (50, 8))  # rysowanie tła
        window.blit(score_icon, (0, 0))


        player.draw()

        current_time = pygame.time.get_ticks()
        for banknote in banknotes:
            if current_time - banknote.spawn_time > 2000:  # Check collision 2 seconds after spawn
                if player.hitbox.colliderect(banknote.hitbox):
                    banknotes.remove(banknote)
                    ouch.play()
                    score += 1

        for banknote in banknotes:
            banknote.draw()

        for enemy in enemies:
            if current_time - enemy.spawn_time > 2000:  # Check collision 2 seconds after spawn
                if player.hitbox.colliderect(enemy.hitbox):
                    enemies.remove(enemy)
                    oof.play()
                    score -= 1
                    unscore +=1

        for enemy in enemies:
            enemy.draw()

        if score % 5 == 0 and score != 0 and score >0:
            if not played:
                levelup.set_volume(0.2)
                levelup.play()
                new_width = player.width + 50
                new_height = player.height + 50

                # Ensure that the new size doesn't exceed the window dimensions
                if new_width <= window.get_width() and new_height <= window.get_height():
                    player.image = pygame.transform.scale(player.image, (new_width, new_height))
                    player.walk_frames_right = [pygame.transform.scale(pygame.image.load(f"animation/frame_{i}.webp"),
                                                                     (new_width, new_height)) for i in
                                              range(1, 12)]
                    player.walk_frames_left = [pygame.transform.scale(
                        pygame.transform.flip(pygame.image.load(f"animation/frame_{i}.webp"), True, False),
                        (new_width, new_height)) for i in
                                             range(1, 12)]

                    player.width = new_width
                    player.height = new_height

                played = True
                levelup_start_time = pygame.time.get_ticks()

            elapsed_time = pygame.time.get_ticks() - levelup_start_time
            if elapsed_time < 3000:  # Display text for 5 seconds (5000 milliseconds)
                levelup_text = pygame.font.Font.render(pygame.font.SysFont('masonserifregular', 70), 'SIŁA +1', True,
                                                       (255, 255, 255))
                window.blit(levelup_text, (window.get_width()/2-150, window.get_height()/2))

        elif played:
            levelup.stop()
            played = False

        if unscore % 5 == 0 and unscore != 0 and unscore >0:
            if not played_unmisc:
                leveldown.set_volume(0.8)
                leveldown.play()
                new_width = player.width-30
                new_height = player.height-30
                score-=2

                # Ensure that the new size doesn't exceed the window dimensions
                if new_width >= 3 and new_height >= 3:
                    player.image = pygame.transform.scale(player.image, (new_width, new_height))
                    player.walk_frames_right = [pygame.transform.scale(pygame.image.load(f"animation/frame_{i}.webp"),
                                                                       (new_width, new_height)) for i in
                                                range(1, 12)]
                    player.walk_frames_left = [pygame.transform.scale(
                        pygame.transform.flip(pygame.image.load(f"animation/frame_{i}.webp"), True, False),
                        (new_width, new_height)) for i in
                        range(1, 12)]
                    player.width = new_width
                    player.height = new_height

                played_unmisc = True
                leveldown_start_time = pygame.time.get_ticks()

            elapsed_time = pygame.time.get_ticks() - leveldown_start_time
            if elapsed_time < 3000:  # Display text for 5 seconds (5000 milliseconds)
                leveldown_text = pygame.font.Font.render(pygame.font.SysFont('masonserifregular', 70), 'SIŁA -2', True,
                                                       (255, 255, 255))
                window.blit(leveldown_text, (window.get_width()/2-150, window.get_height()/2))

        elif played_unmisc:
            leveldown.stop()
            played_unmisc = False


        pygame.display.update()
        pygame.display.flip()

    print(score)


if __name__ == "__main__":
    main()