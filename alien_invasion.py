import sys
from time import sleep

import pygame

from ship import Ship
from settings import Settings
from game_stats import GameStats
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Class to manage game assests and behavior"""

    def __init__(self):
        """Initializing game, create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Instance to store game stats
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  # Group of bullets
        self.aliens = pygame.sprite.Group()  # Group of aliens

        self._create_fleet()

        # Background color
        self.bg_color = (230, 230, 230)

        # Start Alien Invasion in active state
        self.game_active = True

    def run_game(self):
        """Start main loop of game"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(120)

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown(event)
                # Detect when right key is released
            elif event.type == pygame.KEYUP:
                self._check_keyup(event)

    def _check_keydown(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create new bullet and add to group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            # Instance of bullet and assign to variable
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update pos of bullets and get rid of old bullets"""
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets above window
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collsions"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullet, create new fleet
            self.bullets.empty()
            self._create_fleet()

        if not self.aliens:
            # Destroy existing bullets nad create new fleet
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """Check if fleet at edge, then update pos"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens-bottom collisions
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to ship being hit by aliens"""
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1
            # Get rid of any bullet and aliens
            self.bullets.empty()
            self.aliens.empty()
            # Create new fleet, center fleet
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.5)
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """Check if any aliens reached bottom of screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create fleet of aliens"""
        # Create alien and keep adding until no room left
        # Spacing is one alien x and one alien y
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x and increment y
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create alien and place it in fleet"""
        new_alien = Alien(self)
        new_alien.x = x_position  # New alien pos
        new_alien.rect.x = x_position  # New alien rect post
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond if any aliens reached an edge"""
        for alien in self.aliens.sprites():  # Check each alien in group
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop entire fleet and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on screen, flip to new screen"""
        # Redraw screen every loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Make most recetly drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
