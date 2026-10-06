import pygame
from game.asset_factory import create_enemy_surface
from game.projectile import WebProjectile, EnergyBlast, Batarang

class Enemy:
    def __init__(self, x, y, enemy_type="web_hero", patrol_distance=160):
        self.x = float(x)
        self.y = float(y)
        self.start_x = float(x)
        self.enemy_type = enemy_type
        self.patrol_distance = patrol_distance
        
        self.direction = 1  # 1 = Right, -1 = Left
        self.vx = 0.0
        self.vy = 0.0
        self.is_alive = True
        self.anim_tick = 0
        self.is_grounded = False

        self.width = 40
        self.height = 40

        self.base_speed = 2.0
        self.health = 1
        self.damage = 15
        
        self.state = "idle" # idle, patrol, aim, attack, cooldown, chase
        self.cooldown_timer = 0.0
        self.speed_multiplier = 1.0
        self.projectiles_to_spawn = [] # list of projectiles to be spawned this frame

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, dt, player, platforms):
        if not self.is_alive:
            return

        self.anim_tick += 1
        self.projectiles_to_spawn.clear()
        
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt

        self.behavior(dt, player)
        self.apply_physics(platforms)

    def behavior(self, dt, player):
        pass # overridden in subclasses

    def apply_physics(self, platforms):
        self.vy += 0.6
        if self.vy > 12.0:
            self.vy = 12.0

        self.x += self.vx
        for p in platforms:
            if not p.is_oneway and self.rect.colliderect(p.rect):
                if self.vx > 0:
                    self.x = p.rect.left - self.width
                    self.direction = -1
                elif self.vx < 0:
                    self.x = p.rect.right
                    self.direction = 1

        self.y += self.vy
        self.is_grounded = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vy > 0 and self.y + self.height - self.vy <= p.rect.top + 10:
                    self.y = p.rect.top - self.height
                    self.vy = 0
                    self.is_grounded = True

    def take_stomp(self):
        self.health -= 1
        if self.health <= 0:
            self.is_alive = False
            return True
        return False

    def get_distance_to_player(self, player):
        dist_x = player.x - self.x
        dist_y = player.y - self.y
        return (dist_x**2 + dist_y**2)**0.5

    def draw(self, surface, camera_offset_x=0, camera_offset_y=0):
        if not self.is_alive:
            return
        render_x = int(self.x - camera_offset_x)
        render_y = int(self.y - camera_offset_y)
        
        # In the future, this should use AssetManager and self.state
        sprite = create_enemy_surface(self.enemy_type, self.width, self.height, self.anim_tick)
        
        if self.direction < 0:
            sprite = pygame.transform.flip(sprite, True, False)
        surface.blit(sprite, (render_x, render_y))


class WebHero(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="web_hero", patrol_distance=160)
        self.base_speed = 2.2
        self.health = 2
        self.damage = 15
        self.attack_range = 320
        self.attack_cooldown = 1.8

    def behavior(self, dt, player):
        dist = self.get_distance_to_player(player)
        effective_speed = self.base_speed * self.speed_multiplier
        
        if dist < self.attack_range and self.cooldown_timer <= 0:
            self.state = "attack"
            self.direction = 1 if player.x > self.x else -1
            self.vx = 0
            
            # Fire web projectile
            proj = WebProjectile(self.x + self.width/2, self.y + self.height/2, player.x + player.width/2, player.y + player.height/2)
            self.projectiles_to_spawn.append(proj)
            self.cooldown_timer = self.attack_cooldown
        else:
            self.state = "patrol"
            self.vx = self.direction * effective_speed
            if abs(self.x - self.start_x) > self.patrol_distance:
                self.direction *= -1
                self.x += self.direction * 2


class BlastHero(Enemy):
    """Iron Man inspired — hovers at range, fires energy blasts, retreats if too close."""
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="blast_hero", patrol_distance=200)
        self.base_speed = 1.8
        self.health = 3
        self.damage = 20
        self.attack_range = 450
        self.attack_cooldown = 2.0

    def behavior(self, dt, player):
        dist = self.get_distance_to_player(player)
        effective_speed = self.base_speed * self.speed_multiplier
        
        # Chase logic
        if dist < self.attack_range:
            self.direction = 1 if player.x > self.x else -1
            
            if dist < 150: # Maintain distance
                self.vx = -self.direction * effective_speed
                self.state = "retreat"
            elif dist > 250:
                self.vx = self.direction * effective_speed
                self.state = "chase"
            else:
                self.vx = 0
                self.state = "aim"
                
            if self.cooldown_timer <= 0:
                self.state = "attack"
                self.vx = 0
                proj = EnergyBlast(self.x + self.width/2, self.y + self.height/2, player.x + player.width/2, player.y + player.height/2)
                self.projectiles_to_spawn.append(proj)
                self.cooldown_timer = self.attack_cooldown
        else:
            self.state = "patrol"
            self.vx = self.direction * effective_speed
            if abs(self.x - self.start_x) > self.patrol_distance:
                self.direction *= -1
                self.x += self.direction * 2


class DarkHero(Enemy):
    """Batman inspired — fast aggressive chaser, throws batarangs, relentless pursuit."""
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="dark_hero", patrol_distance=180)
        self.base_speed = 3.0
        self.health = 3
        self.damage = 25
        self.attack_range = 380
        self.attack_cooldown = 1.5

    def behavior(self, dt, player):
        dist = self.get_distance_to_player(player)
        effective_speed = self.base_speed * self.speed_multiplier
        
        if dist < self.attack_range:
            self.direction = 1 if player.x > self.x else -1
            self.vx = self.direction * (effective_speed * 1.2)
            self.state = "chase"
            
            if self.cooldown_timer <= 0:
                self.state = "attack"
                proj = Batarang(self.x + self.width/2, self.y + self.height/2, player.x + player.width/2, player.y + player.height/2)
                self.projectiles_to_spawn.append(proj)
                self.cooldown_timer = self.attack_cooldown
        else:
            self.state = "patrol"
            self.vx = self.direction * effective_speed
            if abs(self.x - self.start_x) > self.patrol_distance:
                self.direction *= -1

def create_enemy(enemy_type, x, y):
    if enemy_type == "web_hero":
        return WebHero(x, y)
    elif enemy_type == "blast_hero":
        return BlastHero(x, y)
    elif enemy_type == "dark_hero":
        return DarkHero(x, y)
    else:
        return WebHero(x, y) # Default
