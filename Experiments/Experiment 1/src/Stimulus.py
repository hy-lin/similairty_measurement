'''
Created on 24.03.2015

@author: Hsuan-Yu Lin
'''
import sdl2
import sdl2.ext
import sdl2.surface
import sdl2.pixels
import numpy.random

class ReedFace(object):
    '''
    classdocs
    '''


    def __init__(self, face_parameters, x, y):
        '''
        Constructor
        '''
        self._mapParameters(face_parameters)
        
        self.surface = None
        self.disp_info = None
        self.x = x
        self.y = y
        
        self.sdl_rect = None
        self.rect = None
        
        self.selecting_mode = 'unselected'
        
    def _mapParameters(self, face_parameters):
        self.eyes_gap = face_parameters[0]
        self.eyes_position = face_parameters[1]
        self.nose_length = face_parameters[2]
        self.mouth_position = face_parameters[3]

        
    def _getSourceRect(self):
        w, h = 160, 240
        x0 = (self.eyes_gap-1) * 3 * w + (self.nose_length-1) * w
        y0 = (self.eyes_position-1) * 3 * h + (self.mouth_position-1) * h
        
        return (x0, y0, w, h)
    
    def updateRect(self):
        self.sdl_rect = sdl2.SDL_Rect(int(self.x - self.surface.w/2), \
                                      int(self.y - self.surface.h/2), \
                                      int(self.surface.w), \
                                      int(self.surface.h))
        
        self.rect = (int(self.x - self.surface.w/2), \
                     int(self.y - self.surface.h/2), \
                     int(self.x + self.surface.w/2), \
                     int(self.y + self.surface.h/2))
        
    def updateFaceSurface(self, faces_surface):
        rect = self._getSourceRect()
        self.surface = sdl2.ext.subsurface(faces_surface, rect)
        sdl2.surface.SDL_SetSurfaceBlendMode(self.surface, sdl2.SDL_BLENDMODE_NONE)
        sdl2.surface.SDL_SetColorKey(self.surface, sdl2.SDL_TRUE, sdl2.pixels.SDL_MapRGB(self.surface.format, 255, 255, 255))

        sdl2.surface.SDL_SetSurfaceColorMod(self.surface, 200, 200, 200)
        self.updateRect()
        
    def isMouseOver(self, x, y):
        if self.rect[0] <= x <= self.rect[2] and self.rect[1] <= y <= self.rect[3]:
            return True
        
        return False
    
    def isOverLapping(self, target):
        if self.rect[0] <= target.rect[2] and \
           self.rect[1] <= target.rect[3] and \
           self.rect[2] >= target.rect[0] and \
           self.rect[3] >= target.rect[1]:
            return True
        
        return False
    
    def randomizePosition(self):
        self.x = int(numpy.random.uniform(self.sdl_rect.w, 1024 - self.sdl_rect.w))
        self.y = int(numpy.random.uniform(self.sdl_rect.h, 768 - self.sdl_rect.h))
        
        self.updateRect()
        
    def draw(self, display):
        if self.surface is None :
            return -1
        
        self.updateRect()
        display.drawSurface(self.surface, self.sdl_rect)
        
        if self.selecting_mode == 'mouse_over':
            display.drawThickFrame(self.x - self.surface.w/2, \
                                   self.y - self.surface.h/2, \
                                   self.x + self.surface.w/2, \
                                   self.y + self.surface.h/2, \
                                   1)
        if self.selecting_mode == 'selecting':
            display.drawThickFrame(self.x - self.surface.w/2, \
                                   self.y - self.surface.h/2, \
                                   self.x + self.surface.w/2, \
                                   self.y + self.surface.h/2, \
                                   2)
                    
    def __del__(self):
        sdl2.SDL_FreeSurface(self.surface)