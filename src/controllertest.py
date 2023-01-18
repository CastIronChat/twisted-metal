from __future__ import annotations

import time

import arcade
import pyglet


class Game(arcade.Window):
    def on_update(self, delta_time):
        if not self.initialized:
            self.initialized = True
            self.joy = pyglet.input.get_joysticks()[0]
            self.joy.open()

            # @(self.joy.device._controls[19].event)
            # def on_press():
            #     print("what")

        joy = self.joy
        print(
            f"x={joy.x}, y={joy.y}, z={joy.z}, rx={joy.rx}, ry={joy.ry}, rz={joy.rz}, buttons={joy.buttons}, hat_x={joy.hat_x}, hat_y={joy.hat_y}"
        )
        # for control in joy.device._controls:
        #     print(joy.device._controls[control].value)


g = Game(100, 100, "Game", enable_polling=True)
g.initialized = False
arcade.run()

# while True:
#     pyglet.clock.tick()

#     for window in pyglet.app.windows:
#         window.switch_to()
#         window.dispatch_events()
#         window.dispatch_event("on_draw")
#         window.flip()
#     print(joy.x, joy.y, joy.z)

# while True:
#     time.sleep(0.1)
#     print(joy.x, joy.y, joy.z)
