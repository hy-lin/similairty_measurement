'''
Created on 23.04.2015

@author: Hsuan-Yu Lin
'''

import os
os.environ['PYSDL2_DLL_PATH'] = 'sdl_dll\\'

import sdl2.ext
import sdl2.sdlgfx
import sdl2.surface
import sdl2.sdlttf
import sdl2.timer
import math
import numpy

class Display(object):
    '''
    classdocs
    '''


    def __init__(self, RESOURCES, exp_parameters):
        '''
        Constructor
        '''
        self.RESOURCES = RESOURCES
        self.exp_parameters = exp_parameters
        
        sdl2.ext.init()
        
        self.fps = sdl2.sdlgfx.FPSManager()
        sdl2.sdlgfx.SDL_initFramerate(self.fps)
        self.window = sdl2.ext.Window('Recognition and Source Recall', (1280, 720), flags = sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)
        self.window_surface = self.window.get_surface()
        self.renderer = sdl2.ext.Renderer(self.window_surface)
        
        self.t0 = sdl2.timer.SDL_GetTicks()
        
        sdl2.sdlttf.TTF_Init()
        self.font = None
        
        self.running = True
        
    def getStimulusRect(self, position):
        cx, cy = self.exp_parameters.window_center
        ang = 2 * math.pi * position / self.exp_parameters.n_position
        x = cx + self.exp_parameters.stimulus_radius * math.cos(ang)
        y = cy + self.exp_parameters.stimulus_radius * math.sin(ang)
        
        x0, y0 = x - self.exp_parameters.stimulus_size/2, y - self.exp_parameters.stimulus_size/2
        x1, y1 = x + self.exp_parameters.stimulus_size/2, y + self.exp_parameters.stimulus_size/2
        
        return (x0, y0, x1, y1)
    
    def clear(self, refresh = False):
        self.renderer.clear(sdl2.ext.Color(200, 200, 200))
        if refresh:
            self.refresh()
        
    def refresh(self):
        self.renderer.present()
        self.window.refresh()
        
    def wait(self, ms):
        t0 = sdl2.timer.SDL_GetTicks()
        while sdl2.timer.SDL_GetTicks()-t0 < ms:
            sdl2.ext.get_events()
            
    def waitFPS(self):
        sdl2.sdlgfx.SDL_framerateDelay(self.fps)
    
    def drawThickLine(self, x0, y0, x1, y1, thickness, color):
        x0, y0, x1, y1, thickness = int(x0), int(y0), int(x1), int(y1), int(thickness)
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x0, y0, x1, y1, thickness, color.r, color.g, color.b, color.a)
    
    def drawThickFrame(self, x0, y0, x1, y1, thickness, color = sdl2.ext.Color(0, 0, 0)):
        x0, y0, x1, y1, thickness, mergin = int(x0), int(y0), int(x1), int(y1), int(thickness), int(thickness/2)
        x0, y0, x1, y1 = x0-mergin, y0-mergin, x1+mergin, y1+mergin
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x0, y0, x1, y0, thickness, color.r, color.g, color.b, color.a)
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x0, y0, x0, y1, thickness, color.r, color.g, color.b, color.a)
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x1, y0, x1, y1, thickness, color.r, color.g, color.b, color.a)
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x0, y1, x1, y1, thickness, color.r, color.g, color.b, color.a)
        
    def drawText(self, text, x = None, y = None, text_color = sdl2.SDL_Color(0, 0, 0), align = 'center-center'):
        if self.font is None:
            self.font = sdl2.sdlttf.TTF_OpenFont(self.RESOURCES.get_path('micross.ttf'), int(self.exp_parameters.font_size))
            
        if x is None:
            x = self.window_surface.w/2
        if y is None:
            y = self.window_surface.h/2
        msg = sdl2.sdlttf.TTF_RenderText_Solid(self.font, text, text_color)
        
        if align == 'center-center':
            msg_rect = sdl2.SDL_Rect(int(x-msg.contents.w/2), int(y-msg.contents.h/2), msg.contents.w, msg.contents.h)
        elif align == 'top-left':
            msg_rect = sdl2.SDL_Rect(x, y, msg.contents.w, msg.contents.h)
        elif align == 'top-right':
            msg_rect = sdl2.SDL_Rect(x-msg.contents.w, y, msg.contents.w, msg.contents.h)
        elif align == 'center-left':
            msg_rect = sdl2.SDL_Rect(x, int(y-msg.contents.h/2), msg.contents.w, msg.contents.h)
        elif align == 'center-right':
            msg_rect = sdl2.SDL_Rect(x-msg.contents.w, int(y-msg.contents.h/2), msg.contents.w, msg.contents.h)
            
        sdl2.surface.SDL_BlitSurface(msg.contents, None, self.window_surface, msg_rect)
        sdl2.SDL_FreeSurface(msg)
        
    def drawSurface(self):
