from pico2d import load_image, get_events, clear_canvas, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE
from assets import asset_path
import game_framework

image = None

def init():
    global image
    image = load_image(asset_path('title.png'))

def finish():
    global image
    image = None

def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            game_framework.quit()
            return
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            import play_mode
            game_framework.change_mode(play_mode)
            return

def update(): pass

def render():
    clear_canvas()
    image.draw(400, 300, 800, 600)
    update_canvas()

def pause(): pass
def resume(): pass


if __name__ == '__main__':
    import sys
    from pico2d import open_canvas, close_canvas

    open_canvas(800, 600)
    try:
        game_framework.run(sys.modules[__name__])
    finally:
        close_canvas()
