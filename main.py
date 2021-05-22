import pyglet
import time

PI_PRECISION_VALUE = 7
PHYSICS_ITERATIONS = 10000

class Cube:
    def __init__(self, mass: int, size: int, vel: float, pos: float):
        self.vel = vel
        self.mass = mass
        self.size = size
        self.x = pos

class Precompute:
    def __init__(self, small: Cube, large: Cube, wall: pyglet.shapes.Rectangle):
        self.sum = small.mass + large.mass
        self.stl = small.mass - large.mass
        self.lts = large.mass - small.mass
        self.dlm = 2 * large.mass
        self.dsm = 2 * small.mass
        self.wall = wall.x + wall.width

class Simulation(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=1200, height=600)
        self.set_caption("π Collision Computation Simulation")
        self.set_icon(pyglet.image.load("icon.png"))
        self.small = Cube(size=200, pos=200, vel=0, mass=1)
        self.large = Cube(size=300, pos=500, vel=-1 / PHYSICS_ITERATIONS, mass=100**(PI_PRECISION_VALUE - 1))
        self.batch = pyglet.graphics.Batch()

        self.drawables = {}
        self.collisions = 0
        self.exectime = 0

    def compute_bounce(self):
        self.small.vel *= -1

    def compute_elastic(self):
        snew = (self.data.stl * self.small.vel + self.data.dlm * self.large.vel) / self.data.sum
        lnew = (self.data.lts * self.large.vel + self.data.dsm * self.small.vel) / self.data.sum
        self.small.vel = snew
        self.large.vel = lnew

    def check_wall_collision(self):
        return self.small.x + self.small.vel < self.data.wall

    def check_cube_collision(self):
        return self.small.x + self.small.size + self.small.vel > self.large.x + self.large.vel

    def on_physics(self):
        if self.check_wall_collision():
            self.compute_bounce()
            self.collisions += 1

        elif self.check_cube_collision():
            self.compute_elastic()
            self.collisions += 1

        else:
            self.small.x += self.small.vel
            self.large.x += self.large.vel

    def on_draw(self):
        self.clear()
        self.drawables["small"].x = self.small.x
        self.drawables["smallmass"].x = self.small.x +  + self.small.size / 2
        self.drawables["large"].x = self.large.x
        self.drawables["largemass"].x = self.large.x + self.large.size / 2

        self.drawables["smallmass"].text = f"{self.small.mass:,}kg"
        self.drawables["largemass"].text = f"{self.large.mass:,}kg"
        self.drawables["counter"].text = f"collisions: {self.collisions:,}"
        self.drawables["debug"].text = f"physics execution time: {self.exectime:05.2f}ms"

        cstr = str(self.collisions)
        self.drawables["estimate"].text = f"π = {cstr[:1]}.{cstr[1:] or 0}"
        self.batch.draw()

        self.exectime = time.time()
        for i in range(PHYSICS_ITERATIONS): self.on_physics()
        self.exectime = (time.time() - self.exectime) * 1000

    def setup(self):
        self.drawables["wall"] = pyglet.shapes.Rectangle(x=100, y=0, width=5, height=600, batch=self.batch)
        self.drawables["floor"] = pyglet.shapes.Rectangle(x=0, y=50, width=1200, height=5, batch=self.batch)
        self.drawables["small"] = pyglet.shapes.Rectangle(x=self.small.x, y=55, width=self.small.size, height=self.small.size, color=(140, 146, 172), batch=self.batch)
        self.drawables["large"] = pyglet.shapes.Rectangle(x=self.large.x, y=55, width=self.large.size, height=self.large.size, color=(178, 190, 181), batch=self.batch)
        self.drawables["smallmass"] = pyglet.text.Label(x=self.small.x + self.small.size / 2, y=63 + self.small.size, anchor_x="center", font_size=6, dpi=192, batch=self.batch)
        self.drawables["largemass"] = pyglet.text.Label(x=self.large.x + self.large.x / 2, y=63 + self.large.size, anchor_x="center", font_size=6, dpi=192, batch=self.batch)
        self.drawables["counter"] = pyglet.text.Label(x=150, y=550, font_size=12, dpi=192, batch=self.batch)
        self.drawables["estimate"] = pyglet.text.Label(x=152.5, y=505, font_size=6, dpi=192, batch=self.batch)
        self.drawables["debug"] = pyglet.text.Label(x=152.5, y=525, font_size=6, dpi=192, batch=self.batch)
        self.data = Precompute(self.small, self.large, self.drawables["wall"])

    def run(self):
        self.setup()
        anon = lambda dt: dt
        pyglet.clock.schedule(anon)
        pyglet.app.run()

if __name__ == "__main__":
    simulator = Simulation()
    simulator.run()
