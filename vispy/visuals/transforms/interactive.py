# -*- coding: utf-8 -*-
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
from __future__ import division

import numpy as np
from .linear import STTransform


class PanZoomTransform(STTransform):
    def __init__(self, canvas=None, aspect=None, **kwargs):
        self._aspect = aspect
        self.attach(canvas)
        STTransform.__init__(self, **kwargs)
        self.on_resize(None)
        
    def attach(self, canvas):
        """ Attach this tranform to a canvas """
        self._canvas = canvas
        canvas.events.resize.connect(self.on_resize)
        canvas.events.mouse_wheel.connect(self.on_mouse_wheel)
        canvas.events.mouse_move.connect(self.on_mouse_move)
        
    @property
    def canvas_tr(self):
        return STTransform.from_mapping(
            [(0, 0), self._canvas.size],
            [(-1, 1), (1, -1)])
        
    def on_resize(self, event):
        """ Resize event """
        if self._aspect is None:
            return
        w, h = self._canvas.size
        aspect = self._aspect / (w / h)
        self.scale = (self.scale[0], self.scale[0] / aspect)
        self.shader_map()

    def on_mouse_move(self, event):
        if event.is_dragging:
            dxy = event.pos - event.last_event.pos
            button = event.press_event.button

            if button == 1:
                dxy = self.canvas_tr.map(dxy)
                o = self.canvas_tr.map([0, 0])
                t = dxy - o
                self.move(t)
            elif button == 2:
                center = self.canvas_tr.map(event.press_event.pos)
                if self._aspect is None:
                    self.zoom(np.exp(dxy * (0.01, -0.01)), center)
                else:
                    s = dxy[1] * -0.01
                    self.zoom(np.exp(np.array([s, s])), center)
                    
            self.shader_map()

    def on_mouse_wheel(self, event):
        self.zoom(np.exp(event.delta * (0.01, -0.01)), event.pos)
