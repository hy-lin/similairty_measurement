'''
Created on 26.09.2016

@author: Hsuan-Yu Lin
'''
import os
os.environ['PYSDL2_DLL_PATH'] = 'sdl_dll\\'

import Display
import Recorder
import Stimulus

import itertools
import numpy.random
import sdl2.ext

class ExpParameters(object):
    '''
    The experiment settings.
    '''
    
    def __init__(self):
        
        self.n_items = 16
        self.items_per_multicomparison = 4
        
        pass

class MultiComparisonTrials(object):
    def __init__(self, stimulus_index):
        self.stimulus_index = stimulus_index
        self.stimulus = []
        
    def setupStimulus(self, stimulus_pool):
        self.stimulus = list(range(len(self.stimulus_index)))
        for i, stimulus_index in enumerate(self.stimulus_index):
            self.stimulus[i] = stimulus_pool[stimulus_index]
            print(self.stimulus[i], stimulus_index)
            
    def run(self, display, recorder):
        self._resetStimulusPosition(display)
        self._getResponse(display, recorder)
        self._recordResponse()
        
        
    def _resetStimulusPosition(self, display):
        overlapping = True
        while overlapping:
            for stimulus in self.stimulus:
                stimulus.randomizePosition(display)
                
            overlapping = False
                
            for stimulus1 in self.stimulus:
                for stimulus2 in self.stimulus:
                    if stimulus1 is not stimulus2:
                        if stimulus1.isOverLapping(stimulus2):
                            overlapping = True

    def _getResponse(self, display, recorder):
        x0, y0 = 0, 0
        commit = False
        selected_stimulus = None

        while not commit:
            display.clear(False)
            
            x1, y1, button = recorder.getMouse()
            dx, dy = x1-x0, y1-y0

            if selected_stimulus is not None:
                selected_stimulus.x += dx
                selected_stimulus.y += dy
                selected_stimulus.updateRect()
                
            mouse_overed = False
            for stimulus in self.stimulus:
                
                if stimulus.isMouseOver(x1, y1) and button == 'left_down' and not mouse_overed:
                    stimulus.selecting_mode = 'selecting'
                    selected_stimulus = stimulus
                    mouse_overed = True
                elif stimulus.isMouseOver(x1, y1) and button == 'left_up':
                    selected_stimulus = None
                    mouse_overed = True
                elif stimulus.isMouseOver(x1, y1) and selected_stimulus is None and not mouse_overed:
                    stimulus.selecting_mode = 'mouse_over'
                    mouse_overed = True
                else:
                    if selected_stimulus is not stimulus:
                        stimulus.selecting_mode = 'unselected'
                        
                stimulus.draw(display)
                
            
            key = recorder.getKeyboard(['space'])
            if key == 'space':
                commit = True
            
            display.waitFPS()
            display.refresh()
    
            x0, y0, = x1, y1

    def _recordResponse(self):
        self.result = []
        for stimulus in self.stimulus:
            self.result.append((stimulus.x, stimulus.y))

class MultiComparison(object):
    '''
    The main class for the MultiComparison session of the experiment
    '''


    def __init__(self, exp_parameters, display, recorder, RESOURCES):
        '''
        Constructor
        '''
        self.exp_parameters = exp_parameters
        
        dummy_exp_parms = None
        self.display = display
        self.recorder = recorder
        self.RESOURCES = RESOURCES
        
        self.faces_surface = sdl2.ext.load_image(self.RESOURCES.get_path('faces.png'))
        
    def constructTrials(self):
        self.trials = []
        self._determiningStimulusCombination()
        
        self._setupStimulus()
        
    def run(self):
        self.trials[0].setupStimulus(self.stimulus)
        self.trials[0].run(self.display, self.recorder)
        
    def _determiningStimulusCombination(self):
        subgroup_size = int(self.exp_parameters.items_per_multicomparison / 2)
        n_subgroups = int(self.exp_parameters.n_items / subgroup_size)
        
        stimulus_pool = numpy.random.permutation(self.exp_parameters.n_items)
        subgroups = []
        for subgroup_index in range(n_subgroups):
            subgroups.append([stimulus_pool[i] for i in range(subgroup_index*subgroup_size, (subgroup_index+1)*subgroup_size)])
        
        trial_by_subgroup = itertools.combinations(range(n_subgroups), 2)
        for subgroup in trial_by_subgroup:
            stimulus_index = subgroups[subgroup[0]] + subgroups[subgroup[1]]
            self.trials.append(MultiComparisonTrials(stimulus_index))
            
            
    def _setupStimulus(self):
        self.stimulus = []
        
        for i in range(self.exp_parameters.n_items):
            i_binary = '{0:04b}'.format(i)
            eyes_gap = int(i_binary[0]) * 2 + 1
            eyes_position = int(i_binary[1]) * 2 + 1
            nose_length = int(i_binary[2]) * 2 + 1
            mouth_position = int(i_binary[3]) * 2 + 1
            print(eyes_gap, eyes_position, nose_length, mouth_position)
            self.stimulus.append(Stimulus.ReedFace([eyes_gap, eyes_position, nose_length, mouth_position], -1, -1))
            
            self.stimulus[i].updateFaceSurface(self.faces_surface)
            print(self.stimulus[i], i)


def _main():
    exp_parameters = ExpParameters()

    RESOURCES = sdl2.ext.Resources('.', 'resources')
    main_display = Display.Display(RESOURCES, exp_parameters)
    recorder = Recorder.Recorder('dummy')
    
    multi_comparison_session = MultiComparison(exp_parameters, main_display, recorder, RESOURCES)
    multi_comparison_session.constructTrials()
    multi_comparison_session.run()

if __name__ == '__main__':
    _main()