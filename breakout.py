import time

W = 800
H = 600
RED = 200, 0, 0
BLUE = 0, 0, 200
GREEN = 0, 200, 0

ball = Rect((W/2, H/2), (30, 30))
ball_dir = 5, -5

bat = Rect(0, 0, 150, 15)
bat.midbottom = screen.centrex, screen.bottom - 10
#~ bat = Rect((W/2, 0.96 * H), (150, 15))
N_BLOCKS = 8
BLOCK_W = W / N_BLOCKS
BLOCK_H = BLOCK_W / 4
BLOCK_COLOURS = RED, GREEN, BLUE

blocks = []
for n_block in range(N_BLOCKS):
    colour = BLOCK_COLOURS[n_block % len(BLOCK_COLOURS)]
    block = Rect(n_block * BLOCK_W, 0, BLOCK_W, BLOCK_H)
    block.colour = colour
    blocks.append(block)

def draw_blocks():
    for block in blocks:
        screen.draw.filled_rect(block, block.colour)

def draw():
    screen.clear()
    screen.draw.filled_rect(ball, RED)
    screen.draw.filled_rect(bat, RED)
    draw_blocks()

def on_mouse_move(pos):
    x, y = pos
    bat.center = (x, bat.center[1])

def on_mouse_down():
    global ball_dir
    x, y = ball_dir
    ball_dir = x * 1.5, y * 1.5

def move(ball):
    """returns a new ball at a new position
    """
    global ball_dir
    dx, dy = ball_dir
    ball.move_ip(dx, dy)

    if ball.x > W or ball.x <= 0:
        ball_dir = -dx, dy

    if ball.y <= 0:
        ball_dir = dx, -dy

    if ball.colliderect(bat):
        sounds.blip.play()
        ball_dir = dx, -abs(dy)

    to_kill = ball.collidelist(blocks)
    if to_kill >= 0:
        sounds.block.play()
        ball_dir = dx, abs(dy)
        blocks.pop(to_kill)

    if not blocks:
        sounds.win.play()
        sounds.win.play()
        time.sleep(1)
        exit()

    if ball.y > H:
        sounds.die.play()
        time.sleep(1)
        exit()

def update():
    move(ball)
