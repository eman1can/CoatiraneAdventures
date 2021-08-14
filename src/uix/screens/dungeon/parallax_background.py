from kivy.uix.floatlayout import FloatLayout

from loading.kv_loader import load_kv
from refs import Refs

load_kv(__name__)


class ParallaxBackground(FloatLayout):
    def __init__(self, floor_data, **kwargs):
        self.register_event_type('on_move')
        super().__init__(**kwargs)
        self.view_width = Refs.app.width
        self.view_height = Refs.app.height
        self.size = self.view_width, self.view_height
        self.node_width = self.view_width
        self.node_height = self.view_height
        self.floor_map = floor_data.get_floor_map()
        self._insert_node = False

        self.updates = 0

        x, y = self.floor_map.get_current_node()
        char = self.floor_map.get_node_char((x, y))
        # self.ax, self.ay = self.width * 0.5, self.height * 0.5
        if char == '╷':
            self.ax, self.ay = self.width * 0.5, self.height * 0.3125
        elif char == '╴':
            self.ax, self.ay = self.width * 0.387, self.height * 0.3125
        elif char == '╶':
            self.ax, self.ay = self.width * 0.613, self.height * 0.3125
        elif char == '╵':
            self.ax, self.ay = self.width * 0.5, self.height * 0.177

        self.mode = -1
        self.update(0, 0)

    def node_to_name(self, x, y):
        try:
            node = self.floor_map.get_node_direction((x, y))
        except KeyError:
            return 'tile_blank.png'

        N = 'N' if node & 1 == 1 else ''
        S = 'S' if node & 2 == 2 else ''
        E = 'E' if node & 4 == 4 else ''
        W = 'W' if node & 8 == 8 else ''
        return f'tile_{N}{S}{E}{W}.png'

    def node_to_bounds(self, x, y, w, h):
        # if y % 2 != 0:
        #     return lambda ax, ay: (0.324 * w) < ax < (0.676 * w)
        # else:
        #     y = int(y / 2)
        node = self.floor_map.get_node_direction((x, y))

        # Skeleton Offset
        # Shadow size is: 130 x 36 at scale 0.125
        # Shadow offset y from center is 153 pixels
        # Shadow offset x from center is 0

        sc = Refs.gc.get_skeleton_scale()
        SX = sc / (1706 * 0.125)
        SY = sc / (960 * 0.125)
        OX = 60 * SX
        OTY = 150 * SY
        OBY = 170 * SY

        CLX = 0.324 + OX
        CRX = 0.676 - OX
        HTX = 0.453 + OTY
        HBX = 0.088 + OBY

        if node == 1:  # N
            return lambda ax, ay: (CLX * w) < ax < (CRX * w) and (HBX * h) < ay
        elif node == 2:  # S
            return lambda ax, ay: (CLX * w) < ax < (CRX * w) and ay < (HTX * h)
        elif node == 3:  # NS
            return lambda ax, ay: (CLX * w) < ax < (CRX * w)
        elif node == 4:  # E
            return lambda ax, ay: (CLX * w) < ax and (HBX * h) < ay < (HTX * h)
        elif node == 5:  # NE
            return lambda ax, ay: ((CLX * w) < ax < (CRX * w) and (HBX * h) < ay) or ((CLX * w) < ax and (HBX * h) < ay < (HTX * h))
        elif node == 6:  # SE
            return lambda ax, ay: ((CLX * w) < ax < (CRX * w) and ay < (HTX * h)) or ((CLX * w) < ax and (HBX * h) < ay < (HTX * h))
        elif node == 7:  # NSE
            return lambda ax, ay: ((CLX * w) < ax < (CRX * w)) or ((CLX * w) < ax and (HBX * h) < ay < (HTX * h))
        elif node == 8:  # W
            return lambda ax, ay: ax < (CRX * w) and (HBX * h) < ay < (HTX * h)
        elif node == 9:  # NW
            return lambda ax, ay: ((CLX * w) < ax < (CRX * w) and (HBX * h) < ay) or (ax < (CRX * w) and (HBX * h) < ay < (HTX * h))
        elif node == 10:  # SW
            return lambda ax, ay: ((CLX * w) < ax < (CRX * w) and ay < (HTX * h)) or (ax < (CRX * w) and (HBX * h) < ay < (HTX * h))
        elif node == 11:  # NSW
            return lambda ax, ay: ((CLX * w) < ax < (CRX * w)) or (ax < (CRX * w) and (HBX * h) < ay < (HTX * h))
        elif node == 12:  # EW
            return lambda ax, ay: (HBX * h) < ay < (HTX * h)
        elif node == 13:  # NEW
            return lambda ax, ay: ((CLX * w) < ax < (CRX * w) and (HBX * h) < ay) or ((HBX * h) < ay < (HTX * h))
        elif node == 14:  # SEW
            return lambda ax, ay: ((CLX * w) < ax < (CRX * w) and ay < (HTX * h)) or ((HBX * h) < ay < (HTX * h))
        elif node == 15:  # NSEW
            return lambda ax, ay: (CLX * w) < ax < (CRX * w) or (HBX * h) < ay < (HTX * h)
        return lambda ax, ay: False

    def hide_node(self, node):
        self.ids[f'node_{node}_background'].opacity = 0
        # self.ids[f'node_{node}_foreground'].opacity = 0

    def show_node(self, node, x, y):
        background = self.node_to_name(x, y)
        self.ids[f'node_{node}_background'].opacity = 1
        # self.ids[f'node_{node}_foreground'].opacity = 1
        self.ids[f'node_{node}_background'].source = f'dungeon/{background}'
        # self.ids[f'node_{node}_foreground'].source = f'dungeon/{foreground}'

    def update_node_pos(self, node, dx, dy):
        # print(node, self.ax + dx, self.ay + dy)
        self.ids[f'node_{node}_background'].pos_hint = {'center_x': (self.node_width - self.ax + dx) / self.node_width, 'center_y': (self.node_height - self.ay + dy) / self.node_height}
        # self.ids[f'node_{node}_foreground'].pos = self.ax + dx, self.ay + dy

    def on_move(self, direction):
        pass

    def update(self, dx, dy):
        x, y = self.floor_map.get_current_node()
        # y *= 2
        # if self._insert_node:
        #     y += 1
        bounds = self.node_to_bounds(x, y, self.node_width, self.node_height)

        if bounds(self.ax + dx * 15, self.ay + dy * 15):
            self.ax += dx * 15
            self.ay += dy * 15
        elif bounds(self.ax, self.ay + dy * 15):
            self.ay += dy * 15
        elif bounds(self.ax + dx * 15, self.ay):
            self.ax += dx * 15
        else:
            return False

        self.updates += 1

        # Check for going off node
        OY = 150 * Refs.gc.get_skeleton_scale() * self.height / (960 * 0.125)
        new_node = False
        if self.ax < 0:
            new_node = True
            self.dispatch('on_move', 8)
            x -= 1
            self.ax += self.width
            # self.floor_map.set_current_node((x, int(y)))
        elif self.ax > self.node_width:
            self.dispatch('on_move', 4)
            new_node = True
            x += 1
            self.ax -= self.width
            # self.floor_map.set_current_node((x, int(y)))
        if self.ay < OY:
            self.dispatch('on_move', 2)
            new_node = True
            y += 1
            self.ay += self.height
            # self.floor_map.set_current_node((x, int(y)))
        elif self.ay > self.node_height + OY:
            self.dispatch('on_move', 1)
            new_node = True
            y -= 1
            self.ay -= self.height
            # self.floor_map.set_current_node((x, int(y)))

        if new_node:
            print(self.updates)
            self.updates = 0


        cx, cy = self.width / 2, self.height / 2
        # In perfect center - Mode 0
        if self.ax == cx and self.ay == cy:
            if self.mode != 0:
                self.mode = 0
                self.show_node(1, x, y)
                self.hide_node(2)
                self.hide_node(3)
                self.hide_node(4)
            self.update_node_pos(1, 0, 0)

        # Center and Right - Mode 1
        if self.ax > cx and self.ay == cy:
            if self.mode != 1:
                self.mode = 1
                self.show_node(1, x, y)
                self.show_node(2, x + 1, y)
                self.hide_node(3)
                self.hide_node(4)
            self.update_node_pos(1, 0, 0)
            self.update_node_pos(2, self.node_width, 0)

        # Center and Left - Mode 2
        if self.ax < cx and self.ay == cy:
            if self.mode != 2:
                self.mode = 2
                self.show_node(1, x, y)
                self.show_node(2, x - 1, y)
                self.hide_node(3)
                self.hide_node(4)
            self.update_node_pos(1, 0, 0)
            self.update_node_pos(2, -self.node_width, 0)

        # Center and Top - Mode 3
        if self.ax == cx and self.ay > cy:
            if self.mode != 3:
                self.mode = 3
                self.show_node(1, x, y)
                self.show_node(2, x, y - 1)
                self.hide_node(3)
                self.hide_node(4)
            self.update_node_pos(1, 0, 0)
            self.update_node_pos(2, 0, self.node_height)

        # Center and Bottom - Mode 4
        if self.ax == cx and self.ay < cy:
            if self.mode != 4:
                self.mode = 4
                self.show_node(1, x, y)
                self.show_node(2, x, y + 1)
                self.hide_node(3)
                self.hide_node(4)
            self.update_node_pos(1, 0, 0)
            self.update_node_pos(2, 0, -self.node_height)

        # Center, Top, Right, Top-Right - Mode 5
        if self.ax > cx and self.ay > cy:
            if self.mode != 5:
                self.mode = 5
                self.show_node(1, x, y)
                self.show_node(2, x, y - 1)
                self.show_node(3, x + 1, y)
                self.show_node(4, x + 1, y - 1)
            self.update_node_pos(1, 0, 0)
            self.update_node_pos(2, 0, self.node_height)
            self.update_node_pos(3, self.node_width, 0)
            self.update_node_pos(4, self.node_width, self.node_height)

        # Center, Bottom, Right, Bottom-Right - Mode 6
        if self.ax > cx and self.ay < cy:
            if self.mode != 6:
                self.mode = 6
                self.show_node(1, x, y)
                self.show_node(2, x, y + 1)
                self.show_node(3, x + 1, y)
                self.show_node(4, x + 1, y + 1)
            self.update_node_pos(1, 0, 0)
            self.update_node_pos(2, 0, -self.node_height)
            self.update_node_pos(3, self.node_width, 0)
            self.update_node_pos(4, self.node_width, -self.node_height)

        # Center, Top, Left, Top-Left - Mode 7
        if self.ax < cx and self.ay > cy:
            if self.mode != 7:
                self.mode = 7
                self.show_node(1, x, y)
                self.show_node(2, x, y - 1)
                self.show_node(3, x - 1, y)
                self.show_node(4, x - 1, y - 1)
            self.update_node_pos(1, 0, 0)
            self.update_node_pos(2, 0, self.node_height)
            self.update_node_pos(3, -self.node_width, 0)
            self.update_node_pos(4, -self.node_width, self.node_height)

        # Center, Bottom, Left, Bottom-Left - Mode 8
        if self.ax < cx and self.ay < cy:
            if self.mode != 8:
                self.mode = 8
                self.show_node(1, x, y)
                self.show_node(2, x, y + 1)
                self.show_node(3, x - 1, y)
                self.show_node(4, x - 1, y + 1)
            self.update_node_pos(1, 0, 0)
            self.update_node_pos(2, 0, -self.node_height)
            self.update_node_pos(3, -self.node_width, 0)
            self.update_node_pos(4, -self.node_width, -self.node_height)
        return True