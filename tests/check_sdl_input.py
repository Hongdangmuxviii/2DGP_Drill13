"""실제 SDL 이벤트와 이미지 렌더링으로 숫자키 입력을 검증한다."""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_RENDER_DRIVER'] = 'software'
import ctypes
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pico2d
from sdl2 import SDL_Event, SDL_KEYDOWN, SDL_PushEvent, SDLK_i, SDLK_0, SDLK_1, SDLK_2, SDLK_KP_1, SDLK_KP_2
import game_framework as gf
import play_mode, item_mode, game_world
from ball import Ball

def press(key):
    event = SDL_Event()
    event.type = SDL_KEYDOWN
    event.key.keysym.sym = key
    event.key.repeat = 0
    assert SDL_PushEvent(ctypes.byref(event)) == 1
    gf.stack[-1].handle_events()

pico2d.open_canvas(800, 600)
try:
    gf.change_mode(play_mode)
    # I를 한 번도 누르지 않은 초기 IDLE에서 위쪽 숫자키로 직접 발사.
    for key, size in ((SDLK_1, 21), (SDLK_2, 41)):
        assert play_mode.boy.state == 'IDLE'
        before = len(game_world.world[1])
        press(key)
        assert gf.stack == [play_mode]
        assert len(game_world.world[1]) == before + 1
        assert game_world.world[1][-1].image is Ball.images[size]
        play_mode.update()
        play_mode.render()
    # 메뉴 중 누운 자세로 정지하고 0으로 복귀하면 일어난다.
    before_x = play_mode.boy.x
    press(SDLK_i)
    assert play_mode.boy.state == 'SLEEP'
    for _ in range(10):
        item_mode.update()
        item_mode.render()
    assert play_mode.boy.x == before_x
    press(SDLK_0)
    assert gf.stack == [play_mode] and play_mode.boy.state == 'IDLE'
    assert play_mode.boy.ball_size == 0
    for menu in (False, True):
        for key, size in ((SDLK_1, 21), (SDLK_2, 41), (SDLK_KP_1, 21), (SDLK_KP_2, 41)):
            play_mode.boy.fall_asleep()
            if menu:
                press(SDLK_i)
                assert gf.stack[-1] is item_mode
                item_mode.render()
            before = len(game_world.world[1])
            press(key)
            assert gf.stack[-1] is play_mode
            assert play_mode.boy.state == 'IDLE'
            assert len(game_world.world[1]) == before + 1
            ball = game_world.world[1][-1]
            assert ball.image is Ball.images[size]
            x = ball.x
            play_mode.update()
            assert ball.x != x
            play_mode.render()
    print('PASS: top-row and keypad 1/2, in play and item modes, wake/fire/move/render')
finally:
    while gf.stack:
        gf.stack.pop().finish()
    pico2d.close_canvas()
