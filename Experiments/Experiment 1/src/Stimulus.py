'''
Created on 24.03.2015

@author: Hsuan-Yu Lin
'''
import sdl2
import sdl2.ext
import sdl2.surface
import sdl2.pixels


class DisplayParameters(object):
    '''
    The class for display parameters.
    Class contains the coordinate the center of the stimulus and the size of the stimulus.  
    '''
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        
        self.x0 = int(self.x - self.size[0]/2)
        self.x1 = int(self.x + self.size[0]/2)
        self.y0 = int(self.y - self.size[1]/2)
        self.y1 = int(self.y + self.size[1]/2)
        
    def getRect(self):
        x0 = int(self.x - self.size[0]/2)
        x1 = int(self.x + self.size[0]/2)
        y0 = int(self.y - self.size[1]/2)
        y1 = int(self.y + self.size[1]/2)

        return sdl2.SDL_Rect(x0, y0, self.size[0], self.size[1])

class ReedFace(object):
    '''
    classdocs
    '''


    def __init__(self, face_parameters):
        '''
        Constructor
        '''
        self._mapParameters(face_parameters)
        
        self.surface = None
        self.disp_info = None
        
    def _mapParameters(self, face_parameters):
        self.eyes_gap = face_parameters[0]
        self.eyes_position = face_parameters[1]
        self.nose_length = face_parameters[2]
        self.mouth_position = face_parameters[3]
        
    def attachDisplayParameters(self, display_parameters):
        self.disp_info = display_parameters
        
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
        
    def draw(self, display):
        if self.surface is None or self.disp_info is None:
            return -1
        
        display.drawSurface(self.surface, self.disp_info.getRect())
#         frame_rect = self.disp_info.getRect()
        display.drawThickFrame(self.disp_info.x0, self.disp_info.y0, self.disp_info.x1, self.disp_info.y1, 5)
        
    def __del__(self):
        sdl2.SDL_FreeSurface(self.surface)