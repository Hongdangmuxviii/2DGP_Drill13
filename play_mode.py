from pico2d import clear_canvas, update_canvas, get_events, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_i, SDLK_1, SDLK_2, SDLK_KP_1, SDLK_KP_2
import game_framework
import game_world
from boy import Boy
from grass import Grass

boy = None
paused_at = 0.0

def init():
    global boy
    game_world.clear()
    boy = Boy()
    game_world.add_object(Grass(), 0)
    game_world.add_object(boy, 1)

def finish():
    global boy
    game_world.clear()
    boy = None

def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            import title_mode
            game_framework.change_mode(title_mode)
            return
        if event.type == SDL_KEYDOWN and event.key == SDLK_i:
            import item_mode
            game_framework.push_mode(item_mode)
            return
        boy.handle_event(event)

def update():
    game_world.update()

def render():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    global paused_at
    paused_at = get_time()
    boy.pressed_keys.clear()
    boy.dir = 0
    if boy.state == 'RUN':
        boy.stop_run()
    elif boy.state == 'SLEEP':
        boy.wake_up()
    boy.idle_started_at = get_time()

def resume():
    boy.idle_started_at += get_time() - paused_at
