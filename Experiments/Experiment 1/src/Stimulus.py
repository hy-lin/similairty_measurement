'''
Created on 24.03.2015

@author: Hsuan-Yu Lin
'''
import sdl2
import sdl2.ext
import sdl2.surface
import sdl2.pixels

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
        
        self.rect = None
        
    def _mapParameters(self, face_parameters):
        self.eyes_gap = face_parameters[0]
        self.eyes_position = face_parameters[1]
        self.nose_length = face_parameters[2]
        self.mouth_position = face_parameters[3]

        
    def _getFaceRect(self):
        w, h = 160, 240
        x0 = (self.eyes_gap-1) * 3 * w + (self.nose_length-1) * w
        y0 = (self.eyes_position-1) * 3 * h + (self.mouth_position-1) * h
        
        return (x0, y0, w, h)
        
    def updateFaceSurface(self, faces_surface):
        rect = self._getFaceRect()
        self.surface = sdl2.ext.subsurface(faces_surface, rect)
        sdl2.surface.SDL_SetSurfaceBlendMode(self.surface, sdl2.SDL_BLENDMODE_NONE)
        sdl2.surface.SDL_SetColorKey(self.surface, sdl2.SDL_TRUE, sdl2.pixels.SDL_MapRGB(self.surface.format, 255, 255, 255))

        sdl2.surface.SDL_SetSurfaceColorMod(self.surface, 200, 200, 200)
        self.rect = sdl2.SDL_Rect(int(self.x - self.surface.w/2), \
                                  int(self.y - self.surface.h/2), \
                                  int(self.surface.w), \
                                  int(self.surface.h))
        
    def draw(self, display):
        if self.surface is None :
            return -1
        
        display.drawSurface(self.surface, self.rect)
        display.drawThickFrame(self.x - self.surface.w/2, \
                               self.y - self.surface.h/2, \
                               self.x + self.surface.w/2, \
                               self.y + self.surface.h/2, \
                               5)
        
    def __del__(self):
        sdl2.SDL_FreeSurface(self.surface)