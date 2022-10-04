import sys

import pygame
from time import sleep

from bullet import Bullet
from alien import Alien


def fire_bullet(ai_settings, screen, ship, bullets, se, stats):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed and stats.game_active :
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        se.bullet_sound.play()


def check_keydown_events(event, ai_settings, screen, ship, bullets, se, stats):
    """Respond to keypresses."""
    # Move the ship to the right.
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    # Move the ship to the left.
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets, se, stats)
    elif event.key == pygame.K_q:
        se.stop_game_music()
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb, se):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            se.stop_game_music()
            sys.exit()

        # check for mouse hover over button
        elif event.type == pygame.MOUSEMOTION:
            # change the cursor when hover over the play button
            check_button_hover(play_button)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb, se)

        elif event.type == pygame.KEYDOWN:
            # Respond to keypresses
            check_keydown_events(event, ai_settings, screen, ship, bullets, se, stats)
        
        elif event.type == pygame.KEYUP:
            # Respond to key releases
            check_keyup_events(event, ship)


def check_button_hover(play_button):
    """Change the mouse cursor when hover over Play button"""
    if play_button.rect.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
bullets, mouse_x, mouse_y, sb, se):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        se.game_start_sound.play()

        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.  
        sb.prep_score()

        # Reset and get new high score, if any
        sb.get_high_score()
        sb.prep_high_score()

        # Reset the game level
        sb.prep_level()

        # Reset number of ships
        sb.prep_ships()
        
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)

        # Reset ship position
        ship.center_ship()


def update_screen(ai_settings, screen, ship, bullets, aliens, bg_image, stats, play_button, sb):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    # screen.fill(ai_settings.bg_color)

    # Added a background image
    screen.blit(bg_image, (0, 0))

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb, se):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb, se)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb, se):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

        check_high_score(stats, sb)

        se.alien_sound.play()

    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

        se.level_up_sound.play()


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)

    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb, se):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard with number of ships left
        sb.prep_ships()
        
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Play sound
        se.ship_sound.play()
        
        # Pause.
        sleep(0.5)
    else:
        # Play game over sound
        se.game_over_sound.play()

        # save the high score
        sb.save_high_score()
        
        stats.game_active = False
        pygame.mouse.set_visible(True)



def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb, se):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb, se)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb, se):
    """
    Check if the fleet is at an edge,
    and then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb, se)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb, se)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    # Drop the entire fleet when reach the edge
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    
    # Chnage direction of the fleet
    ai_settings.fleet_direction *= -1


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
