from pico2d import open_canvas, close_canvas
import game_framework
import logo_mode

def main():
    open_canvas(800, 600)
    try:
        game_framework.run(logo_mode)
    finally:
        close_canvas()

if __name__ == '__main__':
    main()
