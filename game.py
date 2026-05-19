import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Default Screen settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
LIGHT_GRAY = (200, 200, 200)

# Paddle settings (pixels per second)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
# Base speeds (will be scaled with resolution)
BASE_PADDLE_SPEED = 420.0  # base ~7 px/frame at 60 FPS -> 420 px/s
BASE_BALL_SPEED = 360.0
BASE_AI_MAX_SPEED = 480.0
# Runtime speeds (may change with resolution)
PADDLE_SPEED = BASE_PADDLE_SPEED

# AI settings (right paddle)
AI_ENABLED = True            # will be set from menu
AI_DIFFICULTY = 0.6         # 0.0 (very weak) .. 1.0 (perfect)
AI_MAX_SPEED = BASE_AI_MAX_SPEED        # max pixels per second AI paddle can move (~8 px/frame)
AI_SMOOTHING = 0.18         # how fast AI target follows predicted target (0..1)
AI_RESPONSE = 10.0          # responsiveness multiplier for AI movement

# Ball settings (pixels per second)
BALL_SIZE = 20
# initial ball speeds (will be recalculated from base)
BALL_SPEED_X, BALL_SPEED_Y = BASE_BALL_SPEED, BASE_BALL_SPEED

# Left paddle
left_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
# Right paddle
right_paddle = pygame.Rect(WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
# Ball (rect)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Floating positions (for sub-pixel / dt-correct movement)
left_y = float(left_paddle.y)
right_y = float(right_paddle.y)
ball_x = float(ball.centerx)
ball_y = float(ball.centery)

# Ball velocities (pixels per second)
ball_vx = BALL_SPEED_X if random.choice((True, False)) else -BALL_SPEED_X
ball_vy = BALL_SPEED_Y if random.choice((True, False)) else -BALL_SPEED_Y

# Scores
left_score = 0
right_score = 0
font = pygame.font.SysFont(None, 50)
menu_font = pygame.font.SysFont(None, 64)
small_font = pygame.font.SysFont(None, 24)

# AI internal state
_ai_target_y = HEIGHT // 2
_ai_last_ball_dir = None
_ai_cooldown = 0

# Progressive speed increase over time
game_speed_multiplier = 1.0
# Base acceleration rate; will be scaled by resolution in apply_display_and_speed_settings
BASE_SPEED_INCREASE_RATE = 0.005  # per second
# Runtime (may be modified by resolution)
SPEED_INCREASE_RATE = BASE_SPEED_INCREASE_RATE
SPEED_MULTIPLIER_MAX = 1.5
# debug flag to confirm main loop started
_game_loop_started = False


def draw(fps_overlay=False, fps_value=0.0):
    SCREEN.fill(BLACK)
    pygame.draw.rect(SCREEN, WHITE, left_paddle)
    pygame.draw.rect(SCREEN, WHITE, right_paddle)
    pygame.draw.ellipse(SCREEN, WHITE, ball)
    # center dividing line removed per earlier request
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    SCREEN.blit(left_text, (WIDTH // 4, 20))
    SCREEN.blit(right_text, (WIDTH * 3 // 4, 20))

    # Current ball speed (pixels/sec) shown top-center
    try:
        speed = math.hypot(ball_vx, ball_vy) * game_speed_multiplier
    except Exception:
        speed = 0.0
    speed_text = small_font.render(f'Rychlost: {speed:.1f}', True, LIGHT_GRAY)
    SCREEN.blit(speed_text, (WIDTH//2 - speed_text.get_width()//2, 8))

    if fps_overlay:
        fps_text = small_font.render(f'FPS: {fps_value:.1f}', True, LIGHT_GRAY)
        SCREEN.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))

    pygame.display.flip()


def draw_menu(selected_index, blink):
    SCREEN.fill(BLACK)
    title = menu_font.render('PING PONG', True, WHITE)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 80))

    options = ['Play vs AI', 'Play 2 Players', 'Settings']
    start_y = 220
    for i, opt in enumerate(options):
        # Render text first to measure size
        text_color = BLACK if i == selected_index else LIGHT_GRAY
        text = font.render(opt, True, text_color)
        text_w, text_h = text.get_width(), text.get_height()
        rect_w = text_w + 40
        rect_h = text_h + 20
        rect_x = WIDTH//2 - rect_w//2
        rect_y = start_y + i*80 - rect_h//2
        if i == selected_index:
            # Draw filled rounded rectangle behind selected option
            pygame.draw.rect(SCREEN, WHITE, (rect_x, rect_y, rect_w, rect_h), border_radius=10)
            SCREEN.blit(text, (WIDTH//2 - text_w//2, rect_y + (rect_h - text_h)//2))
        else:
            # Draw only the text for unselected options
            SCREEN.blit(text, (WIDTH//2 - text_w//2, rect_y + (rect_h - text_h)//2))

    hint = "Use ↑/↓ or W/S to choose. Press Enter to start."
    hint_text = pygame.font.SysFont(None, 28).render(hint, True, GRAY)
    SCREEN.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2, HEIGHT - 60))

    # blinking "Press Enter" indicator
    if blink:
        go_text = font.render('Press Enter', True, WHITE)
        SCREEN.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT - 120))

    pygame.display.flip()


def draw_settings(selected_index, blink, difficulty_index, difficulty_names, FIXED_FPS, fullscreen, resolution_index, resolution_names, fps_overlay):
    SCREEN.fill(BLACK)
    title = menu_font.render('SETTINGS', True, WHITE)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 60))

    opts = [f'AI Difficulty: {difficulty_names[difficulty_index]}', f'Fixed FPS: {FIXED_FPS}', f'Fullscreen: {"On" if fullscreen else "Off"}', f'Resolution: {resolution_names[resolution_index]}', f'FPS Overlay: {"On" if fps_overlay else "Off"}', 'Back']
    start_y = 180
    for i, opt in enumerate(opts):
        text_color = BLACK if i == selected_index else LIGHT_GRAY
        text = font.render(opt, True, text_color)
        text_w, text_h = text.get_width(), text.get_height()
        rect_w = text_w + 40
        rect_h = text_h + 20
        rect_x = WIDTH//2 - rect_w//2
        rect_y = start_y + i*70 - rect_h//2
        if i == selected_index:
            pygame.draw.rect(SCREEN, WHITE, (rect_x, rect_y, rect_w, rect_h), border_radius=10)
            SCREEN.blit(text, (WIDTH//2 - text_w//2, rect_y + (rect_h - text_h)//2))
        else:
            SCREEN.blit(text, (WIDTH//2 - text_w//2, rect_y + (rect_h - text_h)//2))

    hint = "←/→ to change, ↑/↓ to move, Esc to return"
    hint_text = pygame.font.SysFont(None, 24).render(hint, True, GRAY)
    SCREEN.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2, HEIGHT - 50))
    pygame.display.flip()


def ball_reset():
    global ball_x, ball_y, ball_vx
    ball_x = WIDTH / 2
    ball_y = HEIGHT / 2
    ball_vx *= -1


def predict_intercept_y(ball_rect, vx, vy, paddle_x):
    """Predict the y coordinate (center) where the ball will be when it reaches paddle_x.
    This accounts for vertical bounces by reflecting the path (unfolding method).
    Returns a float y position (0..HEIGHT).
    """
    # Use center position for prediction
    bx = float(ball_rect.centerx)
    by = float(ball_rect.centery)
    if vx == 0:
        return by
    t = (paddle_x - bx) / vx
    if t <= 0:
        # ball moving away or already past: return center
        return HEIGHT / 2
    projected = by + vy * t
    period = 2 * HEIGHT
    # normalize into [0, period)
    p = projected % period
    if p < 0:
        p += period
    # reflect if beyond HEIGHT
    if p > HEIGHT:
        return period - p
    else:
        return p


# Clock and fixed-timestep settings
clock = pygame.time.Clock()
FIXED_FPS = 60
FIXED_DT = 1.0 / FIXED_FPS
MAX_FRAME_TIME = 0.25  # clamp to avoid spiral of death

# Start menu loop (main menu now includes Settings)
menu_active = True
menu_choice = 0  # 0 = vs AI, 1 = 2 players, 2 = Settings
blink_timer = 0

# Settings state
difficulty_names = ['Easy', 'Medium', 'Hard']
difficulty_values = [0.35, 0.6, 0.9]
difficulty_index = 1  # default Medium
fps_options = [30, 60, 120]
fps_index = 1  # default 60

# New display-related settings
resolution_options = [(800,600),(1024,768),(1280,720),(1366,768),(1920,1080)]
resolution_names = [f"{w}x{h}" for (w,h) in resolution_options]
resolution_index = 0  # default matches initial WIDTH/HEIGHT
fullscreen = False
fps_overlay = False

# Apply defaults
AI_DIFFICULTY = difficulty_values[difficulty_index]
FIXED_FPS = fps_options[fps_index]
FIXED_DT = 1.0 / FIXED_FPS


def apply_display_and_speed_settings(w, h, make_fullscreen=False):
    """Apply WIDTH/HEIGHT, recreate SCREEN and rescale speeds slightly based on resolution.
    Larger resolutions make the game a bit faster.
    """
    global SCREEN, WIDTH, HEIGHT, left_paddle, right_paddle, left_y, right_y, ball_x, ball_y
    global PADDLE_SPEED, BALL_SPEED_X, BALL_SPEED_Y, AI_MAX_SPEED

    flags = pygame.FULLSCREEN if make_fullscreen else 0
    SCREEN = pygame.display.set_mode((w, h), flags)
    WIDTH, HEIGHT = w, h

    # reposition paddles/ball roughly centered
    left_paddle.x = 30
    right_paddle.x = WIDTH - 40
    left_y = float(HEIGHT//2 - PADDLE_HEIGHT//2)
    right_y = float(HEIGHT//2 - PADDLE_HEIGHT//2)
    ball_x = WIDTH/2
    ball_y = HEIGHT/2

    # scale speeds by screen area ratio
    base_area = 800 * 600
    area = max(1, WIDTH * HEIGHT)
    area_ratio = area / base_area
    # small scaling for paddles/AI, larger scaling for ball and acceleration
    speed_factor = 1.0 + 0.2 * (area_ratio - 1.0)  # paddle / AI
    ball_speed_factor = 1.0 + 0.35 * (area_ratio - 1.0)  # ball starting speed scales more
    accel_factor = 1.0 + 0.5 * (area_ratio - 1.0)  # acceleration scales strongest

    PADDLE_SPEED = BASE_PADDLE_SPEED * speed_factor
    AI_MAX_SPEED = BASE_AI_MAX_SPEED * speed_factor

    # Update ball base speeds and current velocities (preserve direction)
    prev_vx = globals().get('ball_vx', 0.0)
    prev_vy = globals().get('ball_vy', 0.0)
    BALL_SPEED_X = BASE_BALL_SPEED * ball_speed_factor
    BALL_SPEED_Y = BASE_BALL_SPEED * ball_speed_factor
    # preserve sign/direction when updating runtime velocities
    if prev_vx != 0:
        globals()['ball_vx'] = BALL_SPEED_X if prev_vx > 0 else -BALL_SPEED_X
    if prev_vy != 0:
        globals()['ball_vy'] = BALL_SPEED_Y if prev_vy > 0 else -BALL_SPEED_Y

    # Scale the progressive speed increase rate so larger screens accelerate faster
    global SPEED_INCREASE_RATE
    SPEED_INCREASE_RATE = BASE_SPEED_INCREASE_RATE * accel_factor


def settings_menu():
    """Unified settings loop used by main menu and pause menu.
    Up/Down to move, Left/Right or A/D to change, Enter to cycle the current option,
    Esc to go back. """
    global difficulty_index, AI_DIFFICULTY, fps_index, FIXED_FPS, FIXED_DT
    global fullscreen, resolution_index, fps_overlay, blink_timer

    settings_active = True
    settings_choice = 0
    while settings_active:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_UP, pygame.K_w):
                    settings_choice = (settings_choice - 1) % 6
                elif ev.key in (pygame.K_DOWN, pygame.K_s):
                    settings_choice = (settings_choice + 1) % 6
                elif ev.key in (pygame.K_LEFT, pygame.K_a):
                    if settings_choice == 0:
                        difficulty_index = (difficulty_index - 1) % len(difficulty_names)
                        AI_DIFFICULTY = difficulty_values[difficulty_index]
                    elif settings_choice == 1:
                        fps_index = (fps_index - 1) % len(fps_options)
                        FIXED_FPS = fps_options[fps_index]
                        FIXED_DT = 1.0 / FIXED_FPS
                    elif settings_choice == 2:
                        fullscreen = not fullscreen
                        w,h = resolution_options[resolution_index]
                        apply_display_and_speed_settings(w, h, make_fullscreen=fullscreen)
                    elif settings_choice == 3:
                        resolution_index = (resolution_index - 1) % len(resolution_options)
                        w,h = resolution_options[resolution_index]
                        apply_display_and_speed_settings(w, h, make_fullscreen=fullscreen)
                    elif settings_choice == 4:
                        fps_overlay = not fps_overlay
                elif ev.key in (pygame.K_RIGHT, pygame.K_d):
                    if settings_choice == 0:
                        difficulty_index = (difficulty_index + 1) % len(difficulty_names)
                        AI_DIFFICULTY = difficulty_values[difficulty_index]
                    elif settings_choice == 1:
                        fps_index = (fps_index + 1) % len(fps_options)
                        FIXED_FPS = fps_options[fps_index]
                        FIXED_DT = 1.0 / FIXED_FPS
                    elif settings_choice == 2:
                        fullscreen = not fullscreen
                        w,h = resolution_options[resolution_index]
                        apply_display_and_speed_settings(w, h, make_fullscreen=fullscreen)
                    elif settings_choice == 3:
                        resolution_index = (resolution_index + 1) % len(resolution_options)
                        w,h = resolution_options[resolution_index]
                        apply_display_and_speed_settings(w, h, make_fullscreen=fullscreen)
                    elif settings_choice == 4:
                        fps_overlay = not fps_overlay
                elif ev.key == pygame.K_RETURN:
                    # Enter cycles current option; Enter on Back exits
                    if settings_choice == 0:
                        difficulty_index = (difficulty_index + 1) % len(difficulty_names)
                        AI_DIFFICULTY = difficulty_values[difficulty_index]
                    elif settings_choice == 1:
                        fps_index = (fps_index + 1) % len(fps_options)
                        FIXED_FPS = fps_options[fps_index]
                        FIXED_DT = 1.0 / FIXED_FPS
                    elif settings_choice == 2:
                        fullscreen = not fullscreen
                        w,h = resolution_options[resolution_index]
                        apply_display_and_speed_settings(w, h, make_fullscreen=fullscreen)
                    elif settings_choice == 3:
                        resolution_index = (resolution_index + 1) % len(resolution_options)
                        w,h = resolution_options[resolution_index]
                        apply_display_and_speed_settings(w, h, make_fullscreen=fullscreen)
                    elif settings_choice == 4:
                        fps_overlay = not fps_overlay
                    elif settings_choice == 5:
                        settings_active = False
                elif ev.key == pygame.K_ESCAPE:
                    settings_active = False

        blink_timer += 1
        blink = (blink_timer // 30) % 2 == 0
        draw_settings(settings_choice, blink, difficulty_index, difficulty_names, FIXED_FPS, fullscreen, resolution_index, resolution_names, fps_overlay)
        clock.tick(60)


def update(dt, keys):
    global left_y, right_y, ball_x, ball_y, ball_vx, ball_vy
    global left_score, right_score, _ai_target_y, _ai_last_ball_dir, _ai_cooldown
    global game_speed_multiplier, _game_loop_started

    if not _game_loop_started:
        print('DEBUG: update() called — game loop started')
        _game_loop_started = True

    # Left paddle movement
    if keys[pygame.K_w] and left_y > 0:
        left_y -= PADDLE_SPEED * dt * game_speed_multiplier
    if keys[pygame.K_s] and left_y + PADDLE_HEIGHT < HEIGHT:
        left_y += PADDLE_SPEED * dt * game_speed_multiplier

    # Right paddle movement or AI
    if not AI_ENABLED:
        if keys[pygame.K_UP] and right_y > 0:
            right_y -= PADDLE_SPEED * dt * game_speed_multiplier
        if keys[pygame.K_DOWN] and right_y + PADDLE_HEIGHT < HEIGHT:
            right_y += PADDLE_SPEED * dt * game_speed_multiplier
    else:
        ball_dir = ball_vx > 0
        if ball_vx > 0:
            raw_target = predict_intercept_y(ball, ball_vx, ball_vy, right_paddle.left)
            max_error = int(120 * (1.0 - AI_DIFFICULTY))
            error = random.randint(-max_error, max_error)
            raw_target += error
        else:
            raw_target = HEIGHT / 2 + random.randint(-30, 30)

        _ai_target_y += (raw_target - _ai_target_y) * AI_SMOOTHING

        if _ai_last_ball_dir is None or _ai_last_ball_dir != ball_dir:
            _ai_cooldown = max(1, int(14 * (1.0 - AI_DIFFICULTY)))
            _ai_last_ball_dir = ball_dir
        elif _ai_cooldown > 0:
            _ai_cooldown -= 1

        desired_delta = _ai_target_y - (right_y + PADDLE_HEIGHT/2)
        move = desired_delta * AI_RESPONSE * dt * game_speed_multiplier
        max_step = AI_MAX_SPEED * dt * game_speed_multiplier
        if move > max_step:
            move = max_step
        if move < -max_step:
            move = -max_step
        right_y += move

    # Ball movement
    ball_x += ball_vx * dt * game_speed_multiplier
    ball_y += ball_vy * dt * game_speed_multiplier

    # Update rects
    left_paddle.y = int(max(0, min(HEIGHT - PADDLE_HEIGHT, left_y)))
    right_paddle.y = int(max(0, min(HEIGHT - PADDLE_HEIGHT, right_y)))
    ball.center = (int(ball_x), int(ball_y))

    # Collisions
    if ball.top <= 0:
        ball_vy *= -1
        ball.top = 0
        ball_y = ball.centery
    if ball.bottom >= HEIGHT:
        ball_vy *= -1
        ball.bottom = HEIGHT
        ball_y = ball.centery

    if ball.colliderect(left_paddle):
        ball_vx *= -1
        ball.left = left_paddle.right
        ball_x = ball.centerx
    if ball.colliderect(right_paddle):
        ball_vx *= -1
        ball.right = right_paddle.left
        ball_x = ball.centerx

    # Scoring
    if ball.left <= 0:
        right_score += 1
        ball_reset()
    if ball.right >= WIDTH:
        left_score += 1
        ball_reset()

    # progressive speed increase
    game_speed_multiplier = min(SPEED_MULTIPLIER_MAX, game_speed_multiplier + SPEED_INCREASE_RATE * dt)



return_to_menu = False

while True:  # outer loop: show menu, then run game; repeat when player returns to menu
    # run menu
    menu_active = True
    menu_choice = 0
    blink_timer = 0
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    menu_choice = (menu_choice - 1) % 3
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    menu_choice = (menu_choice + 1) % 3
                if event.key == pygame.K_RETURN:
                    if menu_choice == 0:
                        AI_ENABLED = True
                        print('MENU: Play vs AI selected')
                        menu_active = False
                    elif menu_choice == 1:
                        AI_ENABLED = False
                        print('MENU: Play 2 Players selected')
                        menu_active = False
                    else:
                        settings_menu()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        blink_timer += 1
        blink = (blink_timer // 30) % 2 == 0
        draw_menu(menu_choice, blink)
        clock.tick(60)

    # After exiting menu, recompute FIXED_DT just in case
    FIXED_DT = 1.0 / FIXED_FPS
    print(f'Exiting menu. AI_ENABLED={AI_ENABLED} FIXED_FPS={FIXED_FPS}')

    # run game loop until player requests return to menu
    accumulator = 0.0
    return_to_menu = False
    while not return_to_menu:
        # frame_time in seconds (time since last loop)
        frame_time = clock.tick(120) / 1000.0  # cap render fps to 120
        if frame_time > MAX_FRAME_TIME:
            frame_time = MAX_FRAME_TIME
        accumulator += frame_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Open in-game pause menu
                paused = True
                pause_choice = 0  # 0 Resume, 1 Settings, 2 Exit (back to menu)
                while paused:
                    for pe in pygame.event.get():
                        if pe.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if pe.type == pygame.KEYDOWN:
                            if pe.key in (pygame.K_UP, pygame.K_w):
                                pause_choice = (pause_choice - 1) % 3
                            if pe.key in (pygame.K_DOWN, pygame.K_s):
                                pause_choice = (pause_choice + 1) % 3
                            if pe.key == pygame.K_RETURN:
                                if pause_choice == 0:
                                    paused = False
                                elif pause_choice == 1:
                                    settings_menu()
                                else:
                                    # Return to main menu
                                    return_to_menu = True
                                    paused = False
                            if pe.key == pygame.K_ESCAPE:
                                paused = False
                    # draw pause menu
                    SCREEN.fill(BLACK)
                    title = menu_font.render('PAUSED', True, WHITE)
                    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 80))
                    pause_opts = ['Resume', 'Settings', 'Exit']
                    start_y = 220
                    for i, opt in enumerate(pause_opts):
                        text_color = BLACK if i == pause_choice else LIGHT_GRAY
                        text = font.render(opt, True, text_color)
                        text_w, text_h = text.get_width(), text.get_height()
                        rect_w = text_w + 40
                        rect_h = text_h + 20
                        rect_x = WIDTH//2 - rect_w//2
                        rect_y = start_y + i*80 - rect_h//2
                        if i == pause_choice:
                            pygame.draw.rect(SCREEN, WHITE, (rect_x, rect_y, rect_w, rect_h), border_radius=10)
                            SCREEN.blit(text, (WIDTH//2 - text_w//2, rect_y + (rect_h - text_h)//2))
                        else:
                            SCREEN.blit(text, (WIDTH//2 - text_w//2, rect_y + (rect_h - text_h)//2))
                    pygame.display.flip()
                    clock.tick(30)

        # Input snapshot for this frame
        keys = pygame.key.get_pressed()

        # Step fixed-timestep updates
        while accumulator >= FIXED_DT:
            update(FIXED_DT, keys)
            accumulator -= FIXED_DT

        # Render
        draw(fps_overlay=fps_overlay, fps_value=clock.get_fps())
