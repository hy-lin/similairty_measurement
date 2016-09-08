'''
Created on 18.03.2015

@author: Hsuan-Yu Lin
'''
import os
os.environ['PYSDL2_DLL_PATH'] = 'sdl_dll\\'

import sdl2.ext
import sdl2.sdlgfx
import sdl2.surface
import sdl2.timer
import sdl2.sdlttf
import Stimulus
import random
import sdl2

sdl2.ext.get_image_formats()

def _main():
    sdl2.ext.init()
    fps = sdl2.sdlgfx.FPSManager()
    sdl2.sdlgfx.SDL_initFramerate(fps)
    sdl2.sdlttf.TTF_Init()
    
#     sdl2.sdlimage.IMG_Init(0)
    RESOURCES = sdl2.ext.Resources('.', 'resources')
    
    window = sdl2.ext.Window('WTF', (800, 600), flags = sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)
    window.show()
    
    font = sdl2.sdlttf.TTF_OpenFont(bytes(RESOURCES.get_path('one47.ttf'), 'utf-8'), 24)
    msg = sdl2.sdlttf.TTF_RenderText_Solid(font, b'HELLO WORLD', sdl2.SDL_Color(0, 0, 0))

    
    window_surface = window.get_surface()
    renderer = sdl2.ext.Renderer(window_surface)
    
    renderer.clear(sdl2.ext.Color(100, 100, 100))
    sdl2.sdlgfx.aalineColor(renderer.renderer, 20, 20, 40, 40, sdl2.ext.Color(255, 90, 109))
    sdl2.sdlgfx.aalineColor(renderer.renderer, 20, 40, 40, 20, sdl2.ext.Color(255, 255, 255))
    
    sdl2.sdlgfx.thickLineColor(renderer.renderer, 40, 40, 80, 80, 5, sdl2.ext.Color(255, 90, 109))
        
    faces_surface = sdl2.ext.load_image(RESOURCES.get_path('faces.png'))
#     sdl2.surface.SDL_SetColorKey(faces_surface, sdl2.SDL_TRUE, sdl2.ext.Color(0, 0, 0))
    face = sdl2.ext.subsurface(faces_surface, (0, 0, 160, 240))
    
    print(type(renderer.renderer))
#     dst_rect = sdl2.rect(0, 0, 180, 240)
    sdl2.surface.SDL_BlitScaled(faces_surface, sdl2.SDL_Rect(0, 0, 160, 240), window_surface, sdl2.SDL_Rect(0, 0, 40, 60))
#     sdl2.surface.SDL_BlitSurface(faces_surface, sdl2.SDL_Rect(0, 0, 160, 240), window_surface, sdl2.SDL_Rect(0, 0, 40, 60))
    
    
#     self.softwaresprite = factory.from_surface(msg.contents, True)
#     self.softwaresprite.position = posx, posy
    
    
    renderer.draw_rect((20, 20, 20, 20), sdl2.ext.rgba_to_color(3567780095))
    
    x, y = window.size[0]/2, window.size[1]/2
    random_face = Stimulus.ReedFace((2, 2, 2, 2))
    random_face.attachDisplayParameters(Stimulus.DisplayParameters(x, y, (60, 90)))
    random_face.updateFaceSurface(faces_surface)
    
    t0 = sdl2.timer.SDL_GetTicks()
    
    window.running = True
    while window.running:
        renderer.clear(sdl2.ext.Color(100, 100, 100))
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                window.running = False
                break
            
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_SPACE:
                    random_face = Stimulus.ReedFace((random.randint(1, 3), random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)))
                    random_face.attachDisplayParameters(Stimulus.DisplayParameters(x, y, (60, 90)))
                    random_face.updateFaceSurface(faces_surface)
        
        random_face.draw(window_surface)
        sdl2.sdlgfx.aalineColor(renderer.renderer, 20, 20, 40, 40, sdl2.ext.Color(255, 90, 109))
        sdl2.sdlgfx.aalineColor(renderer.renderer, 20, 40, 40, 20, sdl2.ext.Color(255, 255, 255))
        
        sdl2.sdlgfx.thickLineColor(renderer.renderer, 40, 40, 80, 80, 5, sdl2.ext.Color(255, 90, 109))
        sdl2.sdlgfx.SDL_framerateDelay(fps)
        sdl2.surface.SDL_BlitSurface(msg.contents, None, window_surface, sdl2.SDL_Rect(0, 0, 20, 20))
        renderer.present()
        window.refresh()
        print(sdl2.timer.SDL_GetTicks() - t0)


if __name__ == '__main__':
    _main()