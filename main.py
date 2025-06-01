import pgzrun
import random
from pygame import Rect

# Configurações principais
WIDTH = 1000  # Largura está fixa em 1000 pixels
HEIGHT = 600  # Altura está fixa em 600 pixels

class Game:
    def __init__(self):
        self.SOUND_ON = True
        self.game_state = "MENU"  # MENU, PLAYING
        self.score = 0 #Pontuacao do Herói 
        self.lives = 3 #Vida padrão do Herói ao iniciar o jogo
        self.setup_game_elements()
        
    def setup_game_elements(self):
        # Configuração do cenário
        self.floor = Rect((0, 580), (WIDTH, 20))
        self.platforms = [
            self.floor,
            Rect((450, 500), (100, 10)),
            Rect((300, 400), (100, 10)),
            Rect((600, 400), (100, 10)),
            Rect((200, 300), (100, 10)),
            Rect((700, 300), (100, 10)),
            Rect((100, 200), (100, 10)),
            Rect((800, 200), (100, 10)),
            Rect((10, 100), (100, 10)),
            Rect((890, 100), (100, 10)),
            Rect((100, 400), (100, 10)),
            Rect((800, 400), (100, 10)),
            Rect((450, 300), (100, 10))
        ]
        
        # Cores
        self.ground_color = (80, 70, 55) 
        self.floor_color = (21, 24, 38)
        
        # Posições das moedas
        self.coin_positions = [
            (950, 70), (50, 70), (850, 170), (150, 170),
            (750, 270), (250, 270), (650, 370), (350, 370), (500, 470)
        ]
        
        # Configuração inicial do áudio
        music.set_volume(1 if self.SOUND_ON else 0)
        music.play('background_music')
    
    def toggle_sound(self):
        self.SOUND_ON = not self.SOUND_ON
        music.set_volume(1 if self.SOUND_ON else 0)
        return "Sons: " + ("ON" if self.SOUND_ON else "OFF")
    
    def start_game(self):
        self.game_state = "PLAYING"
        self.score = 0
        self.lives = 3
    
    def draw_menu(self):
        screen.fill((0, 69, 56))
        
        # Título do jogo
        screen.draw.text("HEROI DA SELVA", 
                        center=(WIDTH/2, 100), 
                        fontsize=60, 
                        color=(255, 255, 255),
                        shadow=(1, 1))
        
        # Botões
        button_y = HEIGHT/2
        screen.draw.filled_rect(Rect((WIDTH/2-100, button_y-70), (200, 40)), (50, 50, 50))
        screen.draw.text("Iniciar Jogo", center=(WIDTH/2, button_y-50), fontsize=30, color=(255, 255, 255))
        
        screen.draw.filled_rect(Rect((WIDTH/2-100, button_y), (200, 40)), (50, 50, 50))
        screen.draw.text("Sons: ON" if self.SOUND_ON else "Sons: OFF", center=(WIDTH/2, button_y+20), fontsize=30, color=(255, 255, 255))
        
        screen.draw.filled_rect(Rect((WIDTH/2-100, button_y+70), (200, 40)), (50, 50, 50))
        screen.draw.text("Sair", center=(WIDTH/2, button_y+90), fontsize=30, color=(255, 255, 255))
        
        # Rodapé
        
        screen.draw.text("Desenvolvido por Marlisson Anjos", 
                        center=(WIDTH/2, HEIGHT-60), 
                        fontsize=20, 
                        color=(150, 150, 150))

class Hero:
    def __init__(self):
        self.actor = Actor('player.gif', (500, 250))
        self.x_velocity = 0
        self.y_velocity = 0
        self.gravity = 1
        self.jumping = False
        self.jumped = False
        self.images = {
            'idle': 'player',
            'left': 'jumper-left',
            'right': 'jumper-right',
            'jump': 'jump'
        }
    
    def update(self):
        # Reset da imagem quando parado
        if self.x_velocity == 0 and not self.jumped and not self.jumping:
            self.actor.image = self.images['idle']
        
        # Movimentação horizontal
        if keyboard.left:
            if self.actor.x > 40 and self.x_velocity > -8:
                self.x_velocity -= 2
                self.actor.image = self.images['left']
        if keyboard.right:
            if self.actor.x < 960 and self.x_velocity < 8:
                self.x_velocity += 2
                self.actor.image = self.images['right']
        
        self.actor.x += self.x_velocity
        
        # Física (atrito)
        if self.x_velocity > 0:
            self.x_velocity -= 1
        if self.x_velocity < 0:
            self.x_velocity += 1
            
        # Gravidade e pulo
        if self.collidecheck():
            self.gravity = 1
            self.actor.y -= 1
        else:
            self.actor.y += self.gravity
            if self.gravity <= 20:
                self.gravity += 0.5
        
        # Pulo
        if keyboard.up and self.collidecheck() and not self.jumped:
            if game.SOUND_ON:
                sounds.jump.play()
            self.jumping = True
            self.jumped = True
            clock.schedule_unique(self.set_jumped_false, 0.4)
            self.actor.image = self.images['jump']
            self.y_velocity = 95
            
        if self.jumping and self.y_velocity > 25:
            self.y_velocity = self.y_velocity - ((100 - self.y_velocity)/2)
            self.actor.y -= self.y_velocity/3 
        else: 
            self.y_velocity = 0
            self.jumping = False
    
    def set_jumped_false(self):
        self.jumped = False
        
    def collidecheck(self):
        for platform in game.platforms:
            if self.actor.colliderect(platform):
                return True
        return False
    
    def draw(self):
        self.actor.draw()

class Coin:
    def __init__(self):
        self.actor = Actor('coin_1.gif')
        self.reset_position()
        
    def reset_position(self):
        pos = random.choice(game.coin_positions)
        self.actor.pos = pos
    
    def draw(self):
        self.actor.draw()

class Enemy:
    def __init__(self, enemy_type):
        self.type = enemy_type
        self.setup_enemy()
        
    def setup_enemy(self):
        if self.type == "flying":
            self.images = ['eyes_monster1', 'eyes_monster2', 'eyes_monster3',
                         'eyes_monster4', 'eyes_monster5', 'eyes_monster6', 'eyes_monster7']
            self.actor = Actor(self.images[0], (0, 100))
            self.speed = 3
            self.direction = 1
        else:  # ground enemy
            self.images = ['dragon1', 'dragon1.1', 'dragon2', 'dragon3',
                          'dragon4', 'dragon5', 'dragon6', 'dragon7', 'dragon8']
            self.actor = Actor(self.images[0], (0, 550))
            self.speed = 1.5
            self.direction = 1
            
        self.frame = 0
        self.animation_speed = 0.2 if self.type == "flying" else 0.1
        self.is_alive = True
        
    def update(self):
        self.animate()
        self.move()
    
    def animate(self):
        self.frame += self.animation_speed
        if self.frame >= len(self.images):
            self.frame = 0
        self.actor.image = self.images[int(self.frame)]
    
    def move(self):
        self.actor.x += self.speed * self.direction

        if self.type == "flying":
            if self.actor.x > WIDTH:
                self.direction = -1
                self.actor.y += 20
            elif self.actor.x < 0:
                self.direction = 1
                
            if self.actor.y < 50:
                self.actor.y = 50
            elif self.actor.y > 150:
                self.actor.y = 100
        else:
            if self.direction == -1:
                self.actor.flip_x = True
            else:
                self.actor.flip_x = False
                
            if self.actor.right > WIDTH:
                self.direction = -1
            elif self.actor.left < 0:
                self.direction = 1
                
            self.actor.y = 550
    
    def draw(self):
        self.actor.draw()

# Inicialização do jogo
game = Game()
hero = Hero()
coin = Coin()
enemies = [Enemy("flying"), Enemy("ground")]

def update():
    if game.game_state == "PLAYING":
        hero.update()
        for enemy in enemies:
            enemy.update()
            
        # Colisão com moeda
        if hero.actor.colliderect(coin.actor):
            if game.SOUND_ON:
                sounds.coin.play()
            game.score += 1
            coin.reset_position()
            
        # Colisão com inimigos
        for enemy in enemies:
            if hero.actor.colliderect(enemy.actor):
                if game.SOUND_ON:
                    sounds.death.play()
                reset_hero_position()

def draw():
    if game.game_state == "MENU":
        game.draw_menu()
    else:
        # Desenhar o jogo
        screen.blit('floresta', (0, 0))
        
        # Plataformas
        for platform in game.platforms:
            color = game.ground_color if platform != game.floor else game.floor_color
            screen.draw.filled_rect(platform, color)
        
        # Itens e personagens
        coin.draw()
        hero.draw()
        for enemy in enemies:
            enemy.draw()
        
        # HUD
        screen.draw.text(f"Pontos: {game.score}", 
                        topleft=(20, 20), 
                        fontsize=30, 
                        color=(255, 255, 255),
                        shadow=(1, 1))
        
        screen.draw.text(f"Vidas: {game.lives}", 
                        topleft=(200, 20), 
                        fontsize=30,
                        color=(255, 255, 255),
                        shadow=(1, 1))

def on_mouse_down(pos):
    if game.game_state == "MENU":
        button_y = HEIGHT/2
        if WIDTH/2-100 <= pos[0] <= WIDTH/2+100:
            if button_y-70 <= pos[1] <= button_y-30:  # Iniciar Jogo
                game.start_game()
            elif button_y <= pos[1] <= button_y+40:  # Sons
                game.toggle_sound()
            elif button_y+70 <= pos[1] <= button_y+110:  # Sair
                exit()

def on_key_down(key):
    if key == keys.ESCAPE:
        if game.game_state == "PLAYING":
            game.game_state = "MENU"
        else:
            exit()

def reset_hero_position():
    hero.actor.pos = (500, 250)
    game.score = max(0, game.score - 1)
    game.lives -= 1
    if game.lives <= 0:
        game.game_state = "MENU"

pgzrun.go()