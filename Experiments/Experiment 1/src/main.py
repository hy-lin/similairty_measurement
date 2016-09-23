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
import Display
import Recorder

sdl2.ext.get_image_formats()

def _main2():
    dummy_exp_parms = None
    RESOURCES = sdl2.ext.Resources('.', 'resources')
    main_display = Display.Display(RESOURCES, dummy_exp_parms)
    recorder = Recorder.Recorder('dummy')
    
    faces_surface = sdl2.ext.load_image(RESOURCES.get_path('faces.png'))
    
    running = True
    t0 = sdl2.timer.SDL_GetTicks()
    
    
    
    faces = []
    for i in range(12):
        reed_face_parameters = (random.randint(1, 3), random.randint(1, 3), random.randint(1, 3), random.randint(1, 3))
        x1 = random.randint(1, main_display.w)
        y1 = random.randint(1, main_display.h)
        random_face = Stimulus.ReedFace(reed_face_parameters, x1, y1)
        random_face.updateFaceSurface(faces_surface)
        
        faces.append(random_face)
    
    selected_stimulus = None
    x0, y0 = 0, 0
    while running:
        frame_t0 = sdl2.timer.SDL_GetTicks() 
        main_display.clear(False)
        
        x1, y1, button = recorder.getMouse()
        dx, dy = x1-x0, y1-y0
        
        
        if selected_stimulus is not None:
            selected_stimulus.x += dx
            selected_stimulus.y += dy
            selected_stimulus.updateRect()
            
        mouse_overed = False
        for face in faces:
            
            if face.isMouseOver(x1, y1) and button == 'left_down':
                face.selecting_mode = 'selecting'
                selected_stimulus = face
                mouse_overed = True
            elif face.isMouseOver(x1, y1) and button == 'left_up':
                selected_stimulus = None
                mouse_overed = True
            elif face.isMouseOver(x1, y1) and selected_stimulus is None and not mouse_overed:
                face.selecting_mode = 'mouse_over'
                mouse_overed = True
            else:
                if selected_stimulus is not face:
                    face.selecting_mode = 'unselected'
            
            face.draw(main_display)
        
        print(sdl2.timer.SDL_GetTicks() - frame_t0)
        main_display.waitFPS()
        main_display.refresh()
        print(sdl2.timer.SDL_GetTicks() - frame_t0)

        x0, y0, = x1, y1
        
        if sdl2.timer.SDL_GetTicks() - t0 > 10000:
            running = False
    


if __name__ == '__main__':
    _main2()