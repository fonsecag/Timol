from __future__ import annotations

from pytermgui import Widget
from pytermgui import tim
from pytermgui.ansi_interface import MouseAction
from scipy.spatial.transform import Rotation
import numpy as np 
from logger import log_write

class PlotWidget(Widget):

    last_width = 0
    last_hegiht = 0
    parent = None
    bg = 'black'
    R = None
    colors = None
    sizes = None
    center = (0,0)
    scale = 20 # line height (i.e. pixel size) per length (pixels are 2x character width or 1x character height)
    yaw = 0
    pitch = 0
    last_mouse_pos = (0,0)
    drag_start_pos = (0,0)
    last_mouse_action = None

    def __init__(self, **attrs) -> None:

        super().__init__(**attrs)
        
        self.locked = True

        self.selected_pixel = None
        self.colors = [self.bg]
        self.build()

    def get_height(self):
        if self.parent is None:
            return 1
        else:
            return self.parent.height

    def get_width(self):
        return self.width // 2

    def get_lines(self) -> list[str]:
        """Returns lines built by the `build` method."""

        if self.get_width() != self.last_width or self.get_height() != self.last_height:
            self.build()

        
        return self._lines

    def build_matrix(self):

        w, h = self.get_width(), self.get_height()
        matrix = np.zeros((h, w)).astype(int)
        if self.R is None:
            return matrix

        R, sizes, distances = self.get_projection()

        x_center, y_center = w/2, h/2

        # from furthest to closest
        # everything gets converted to pixel space
        for idx in np.argsort(-distances):
            x, y = R[idx] * self.scale
            x += x_center
            y += y_center

            pixel_size = sizes[idx] * self.scale

            x_min = max(0, int(np.round(x - pixel_size)))
            x_max = min(w-1, int(np.round(x + pixel_size)))

            y_min = max(0, int(np.round(y - pixel_size)))
            y_max = min(h-1, int(np.round(y + pixel_size)))


            row_idxs, col_idxs = [], []
            for xn in range(x_min, x_max):
                for yn in range(y_min, y_max):
                    if np.sqrt((xn + 0.5 - x)**2 + (yn + 0.5 - y)**2) > pixel_size:
                        continue
                    
                    col_idxs.append(xn)
                    row_idxs.append(yn)

            matrix[row_idxs, col_idxs] = idx + 1 # 0 is background

        return np.flip(matrix, axis = 0)
        
    def build(self) -> list[str]:

        lines = []

        # lines = [f"[@{self.bg}] "*self.width] * self.get_height()
        matrix = self.build_matrix()
        for i in range(matrix.shape[0]):
            line = ''
            last_idx = -1
            for j in range(matrix.shape[1]):
                idx = matrix[i][j]
                if idx != last_idx:
                    line += f"[@{self.colors[idx]}]"
                    last_idx = idx
                line += "  "
            
            lines.append(line)

        self._lines = [tim.parse(x) for x in lines]
        self.last_width = self.get_width()
        self.last_height = self.get_height()
        self.width = self.get_width() * 2
        self.height = self.get_height()
        return lines

    def get_projection(self):
        '''
        Very rudimentary orthographic projection along the x-axis for the sake
        of simplicity and efficiency. 
        '''

        rot = Rotation.from_euler('zyx', [self.yaw, self.pitch, 0], degrees = True)
        R = rot.apply(self.R)
        return R[:,1:], self.sizes, R[:,0]

    def set_spheres(self, R, sizes, colors):
        self.R = R 
        self.sizes = sizes
        self.colors = [self.bg] + colors

        self.build()

    def scroll(self, scroll_up, pos):

        if self.last_mouse_action != MouseAction.RELEASE:
            return

        if scroll_up:
            self.scale += 1
        else:
            self.scale = max(1, self.scale - 1)

        self.build()

    def drag(self, pos):
        pass
        # log_write(f"Drag {pos}")
        # self.drag_start_pos = pos

    def release_mouse(self, pos):
        # log_write(f'Release {pos}')
        
        if self.last_mouse_action == MouseAction.LEFT_DRAG:
            x0, y0 = self.last_mouse_pos
            x, y = pos

            dx, dy = x - x0, y-y0

            log_write(f'{dx}, {dy}')
            self.yaw -= 5 * dx
            self.pitch += 5 * dy
            # self.drag_start_pos = pos
            self.build()

        self.last_mouse_pos = pos

    def handle_mouse(self, event):
        
        action = event.action
        if action == MouseAction.SCROLL_UP or action == MouseAction.SCROLL_DOWN:
            self.scroll(
                action == MouseAction.SCROLL_UP,
                event.position
            )


        elif action == MouseAction.LEFT_DRAG:
            self.drag(event.position)

        elif action == MouseAction.RELEASE:
            self.release_mouse(event.position)

        log_write(f'{action}, {event.position}')

        self.last_mouse_action = action
        # else:
        #     log_write(f'{action}, {event.position}')
