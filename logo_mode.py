from pico2d import load_image, get_time, get_events, clear_canvas, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE
from assets import asset_path
import game_framework

image = None
logo_start_time = 0.0

def init():
    global image, logo_start_time
    image = load_image(asset_path('tuk_credit.png'))
    logo_start_time = get_time()

def finish():
    global image
    image = None

def update():
    if get_time() - logo_start_time >= 2.0:
        import title_mode
        game_framework.change_mode(title_mode)

def render():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            game_framework.quit()
            return

def pause(): pass
def resume(): pass
