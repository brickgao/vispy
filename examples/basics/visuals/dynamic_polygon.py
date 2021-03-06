# -*- coding: utf-8 -*-
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

"""
Demonstration of Polygon and subclasses
"""

import sys
import numpy as np

from vispy import app, gloo, visuals
from vispy.visuals import transforms

# vertex positions of polygon data to draw
pos = np.array([[0, 0, 0],
               [0.25, 0.22, 0],
               [0.25, 0.5, 0],
               [0, 0.5, 0],
               [-0.25, 0.25, 0]])

pos = np.array([[0, 0],
                [10, 0],
                [10, 10],
                [20, 10],
                [20, 20],
                [25, 20],
                [25, 25],
                [20, 25],
                [20, 20],
                [10, 17],
                [5, 25],
                [9, 30],
                [6, 15],
                [15, 12.5],
                [0, 5]])

theta = np.linspace(0, 2*np.pi, 11)
pos = np.hstack([np.cos(theta)[:, np.newaxis],
                 np.sin(theta)[:, np.newaxis]])
pos[::2] *= 0.4
pos[-1] = pos[0]


class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, keys='interactive', size=(800, 800))
        global pos
        self.visuals = []
        polygon = visuals.PolygonVisual(pos=pos, color=(0.8, .2, 0, 1),
                                        border_color=(1, 1, 1, 1))
        polygon.transform = transforms.STTransform(scale=(200, 200),
                                                   translate=(600, 600))
        self.visuals.append(polygon)

        ellipse = visuals.EllipseVisual(pos=(0, 0, 0), radius=(100, 100),
                                        color=(0.2, 0.2, 0.8, 1),
                                        border_color=(1, 1, 1, 1),
                                        start_angle=180., span_angle=150.)
        ellipse.transform = transforms.STTransform(scale=(0.9, 1.5),
                                                   translate=(200, 200))
        self.visuals.append(ellipse)

        rect = visuals.RectangleVisual(pos=(600, 200, 0), height=200.,
                                       width=300.,
                                       radius=[30., 30., 0., 0.],
                                       color=(0.5, 0.5, 0.2, 1),
                                       border_color='white')
        rect.transform = transforms.NullTransform()
        self.visuals.append(rect)

        rpolygon = visuals.RegularPolygonVisual(pos=(200., 600., 0), 
                                                radius=160,
                                                color=(0.2, 0.8, 0.2, 1),
                                                border_color=(1, 1, 1, 1),
                                                sides=6)
        rpolygon.transform = transforms.NullTransform()
        self.visuals.append(rpolygon)

        for v in self.visuals:
            v.tr_sys = transforms.TransformSystem(self)
            v.tr_sys.visual_to_document = v.transform

        self._timer = app.Timer('auto', connect=self.on_timer, start=True)

        self.show()

    def on_draw(self, ev):
        gloo.set_clear_color((0, 0, 0, 1))
        gloo.set_viewport(0, 0, *self.physical_size)
        gloo.clear()
        for vis in self.visuals:
            vis.draw(vis.tr_sys)

    def on_timer(self, event):
        polygon, ellipse, rect, rpolygon = self.visuals
        r = ellipse.radius
        ellipse.radius = r[0], r[1] + np.sin(event.elapsed * 10)
        ellipse.span_angle = (ellipse.span_angle + 100. * event.dt) % 360
        
        polygon.color = (0.3 * (0.5 + np.sin(event.elapsed*2 + 0)),
                         0.3 * (0.5 + np.sin(event.elapsed*2 + np.pi * 2./3.)),
                         0.3 * (0.5 + np.sin(event.elapsed*2 + np.pi * 4./3.)),
                         )
        polygon.border_color = (.8, .8, .8, 
                                0.5 + (0.5 * np.sin(event.elapsed*10)))
        
        rpolygon.radius = 100 + 10 * np.sin(event.elapsed * 3.1)
        rpolygon.sides = int(20 + 17 * np.sin(event.elapsed))
        
        self.update()


if __name__ == '__main__':
    win = Canvas() 
    if sys.flags.interactive != 1:
        win.app.run()
