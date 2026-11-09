from pico2d import get_canvas_width, load_image
from assets import asset_path
import game_world

class Ball:
    images = {}

    def __init__(self, x, y, velocity, size=21):
        if size not in (21, 41):
            raise ValueError('Ball size must be 21 or 41')
        if size not in Ball.images:
            Ball.images[size] = load_image(asset_path(f'ball{size}x{size}.png'))
        self.image = Ball.images[size]
        self.x, self.y, self.velocity = x, y, velocity

    def update(self):
        self.x += self.velocity
        if self.x < 0 or self.x > get_canvas_width():
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)
