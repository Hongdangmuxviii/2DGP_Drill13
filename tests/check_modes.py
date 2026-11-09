"""화면 없이 실제 모드/월드/캐릭터의 전환과 상태 보존을 검증한다."""
import sys
import types
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
clock = [0.0]
events = []
class Image:
    def draw(self, *args): pass
    def clip_draw(self, *args): pass
    def clip_composite_draw(self, *args): pass
pico = types.ModuleType('pico2d')
pico.load_image = lambda path: Image() if Path(path).is_file() else (_ for _ in ()).throw(FileNotFoundError(path))
pico.get_time = lambda: clock[0]
pico.get_canvas_width = lambda: 800
pico.get_events = lambda: events[:]
pico.clear_canvas = pico.update_canvas = lambda: None
sys.modules['pico2d'] = pico
from sdl2 import SDL_KEYDOWN, SDL_QUIT, SDLK_SPACE, SDLK_ESCAPE, SDLK_i, SDLK_0, SDLK_1, SDLK_2
import game_framework as gf
import game_world as world
import logo_mode, title_mode, play_mode, item_mode

def key(k):
    events[:] = [types.SimpleNamespace(type=SDL_KEYDOWN, key=k)]
    gf.stack[-1].handle_events()
    events.clear()

gf.running = True
gf.change_mode(logo_mode)
clock[0] = 1.99
logo_mode.update()
assert gf.stack == [logo_mode]
clock[0] = 2
logo_mode.update()
assert gf.stack == [title_mode]
key(SDLK_SPACE)
boy = play_mode.boy
boy.x = 123
for k,size in [(SDLK_0,0),(SDLK_1,21),(SDLK_2,41)]:
    key(SDLK_i)
    assert gf.stack == [play_mode,item_mode]
    item_mode.render()
    before_selection = len(world.world[1])
    key(k)
    assert len(world.world[1]) == before_selection + (size != 0)
    if size:
        assert world.world[1][-1].image is __import__('ball').Ball.images[size]
    assert gf.stack == [play_mode] and play_mode.boy is boy
    assert boy.x == 123 and boy.ball_size == size
    before = len(world.world[1]);boy.fire_ball()
    assert len(world.world[1]) == before + (size != 0)
# 수면 직전/수면 중 아이템 선택 후 실제 Space 이벤트로 발사한다.
for asleep in (False, True):
    for choice, size in ((SDLK_1, 21), (SDLK_2, 41)):
        if boy.state == 'SLEEP':
            boy.wake_up()
        clock[0] = boy.idle_started_at + (5.1 if asleep else 4.99)
        boy.update()
        key(SDLK_i)
        assert boy.state == 'SLEEP', 'Menu must pause the character lying down'
        clock[0] += 10
        before_selection = len(world.world[1])
        key(choice)
        assert len(world.world[1]) == before_selection + 1
        selected_ball = world.world[1][-1]
        assert selected_ball.image is __import__('ball').Ball.images[size]
        old_x = selected_ball.x
        selected_ball.update()
        assert selected_ball.x != old_x
        clock[0] += 0.02
        boy.update()
        assert boy.state == 'IDLE', ('selection left boy asleep', asleep, size)
        before = len(world.world[1])
        key(SDLK_SPACE)
        assert len(world.world[1]) == before + 1
        ball = world.world[1][-1]
        assert ball.image is __import__('ball').Ball.images[size]
        old_x = ball.x
        ball.update()
        assert ball.x != old_x
# 잠든 상태에서도 Space 한 번으로 일어나 발사한다.
clock[0] = boy.idle_started_at + 5.1
boy.update()
assert boy.state == 'SLEEP'
before = len(world.world[1])
key(SDLK_SPACE)
assert boy.state == 'IDLE' and len(world.world[1]) == before + 1
key(SDLK_ESCAPE)
assert gf.stack == [title_mode] and not any(world.world)
key(SDLK_SPACE)
assert play_mode.boy is not boy
key(SDLK_i)
events[:] = [types.SimpleNamespace(type=SDL_QUIT)]
item_mode.handle_events()
assert not gf.running
while gf.stack: gf.stack.pop().finish()
assert not any(world.world)
# quit/pop 중 종료한 모드의 update/render가 호출되면 실패한다.
for operation in [gf.quit, gf.pop_mode]:
    calls=[]
    mode=types.SimpleNamespace(init=lambda:None, finish=lambda:calls.append('finish'),
        handle_events=operation, update=lambda:calls.append('update'), render=lambda:calls.append('render'))
    gf.run(mode)
    assert calls == ['finish'], calls
print('PASS: logo timing, title/play transitions, item choices, preserved state, cleanup, safe exit')
