from assets import asset_path
from pico2d import load_image


class Grass:
    def __init__(self):
        self.image = load_image(asset_path('grass.png'))

    def draw(self):
        self.image.draw(400, 30)

    def update(self):
        pass
