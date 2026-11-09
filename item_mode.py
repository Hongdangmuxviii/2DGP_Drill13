from pico2d import load_image, get_events, clear_canvas, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_0, SDLK_1, SDLK_2, SDLK_KP_0, SDLK_KP_1, SDLK_KP_2
from assets import asset_path
import game_framework
import game_world
import play_mode

image = None

def init():
    global image
    image = load_image(asset_path('item_select.png'))

def finish():
    global image
    image = None

def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        if event.type == SDL_KEYDOWN:
            sizes = {SDLK_0: 0, SDLK_1: 21, SDLK_2: 41,
                     SDLK_KP_0: 0, SDLK_KP_1: 21, SDLK_KP_2: 41}
            if event.key in sizes:
                play_mode.boy.ball_size = sizes[event.key]
                game_framework.pop_mode()
                # 선택은 새 입력이다. 복귀 후 수면 타이머를 다시 시작한다.
                if play_mode.boy.state == 'SLEEP':
                    play_mode.boy.wake_up()
                else:
                    play_mode.boy.on_enter_IDLE()
                if sizes[event.key]:
                    play_mode.boy.fire_ball()
                return
            if event.key == SDLK_ESCAPE:
                game_framework.pop_mode()
                return

def update(): pass

def render():
    clear_canvas()
    game_world.render()
    image.draw(400, 300)
    update_canvas()

def pause(): pass
def resume(): pass
