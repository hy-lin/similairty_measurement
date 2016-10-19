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
import math

class ExpParameters(object):
    '''
    The experiment settings.
    '''
    
    def __init__(self):
        
        self.n_items = 16
        self.items_per_multicomparison = 8
        
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
        display.wait(300)
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
            self.result.append((stimulus.index, stimulus.x, stimulus.y))
            
        print(self.result)
        
    def findResponseMinMax(self):
        max_x, max_y = -1, -1
        min_x, min_y = 9999, 9999
        for result in self.result:
            if result[1] > max_x:
                max_x = result[1]
            if result[1] < min_x:
                min_x = result[1]
                
            if result[2] > max_y:
                max_y = result[2]
            if result[2] < min_y:
                min_y = result[2]
                
        return min_x, min_y, max_x, max_y
                    
        
class ExperimentSession(object):
    def __init__(self, exp_parameters, display, recorder, RESOURCES):
        '''
        Constructor
        '''
        self.exp_parameters = exp_parameters
        
        self.display = display
        self.recorder = recorder
        self.RESOURCES = RESOURCES
        
        self.faces_surface = sdl2.ext.load_image(self.RESOURCES.get_path('faces.png'))
        
    def constructTrials(self):
        self.trials = []
        self._determiningStimulusCombination()
        
        self._setupStimulusSurface()
        
    def __determiningStimulusCombination(self):
        print('If you see this, I fucked up. Please inform experimenter.')
        raise NameError('Function: __determiningStimulusCombination is not defined in class: ExperimentSession')
        
    def _setupStimulusSurface(self):
        self.stimulus = []
        
        for i in range(self.exp_parameters.n_items):
            i_binary = '{0:04b}'.format(i)
            eyes_gap = int(i_binary[0]) * 2 + 1
            eyes_position = int(i_binary[1]) * 2 + 1
            nose_length = int(i_binary[2]) * 2 + 1
            mouth_position = int(i_binary[3]) * 2 + 1
            print(eyes_gap, eyes_position, nose_length, mouth_position)
            self.stimulus.append(Stimulus.ReedFace([eyes_gap, eyes_position, nose_length, mouth_position], -1, -1, i))
            
            self.stimulus[i].updateFaceSurface(self.faces_surface)
            print(self.stimulus[i], i)

class MultiComparison(ExperimentSession):
    '''
    The main class for the MultiComparison session of the experiment
    '''

    def run(self):
        for trial in self.trials:
            trial.setupStimulus(self.stimulus)
            trial.run(self.display, self.recorder)
        
        
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
            
    def save(self, pID):
        dist_matrix = [[[]for m in range(self.exp_parameters.n_items)] for n in range(self.exp_parameters.n_items)]
        for trial in self.trials:
            min_x, min_y, max_x, max_y = trial.findResponseMinMax()
            x_scale = 1280.0/(max_x - min_x)
            y_scale = 1024.0/(max_y - min_y)
            
            for result_i in trial.result:
                for result_l in trial.result:
                    i, l = result_i[0], result_l[0]
                    x_i, x_l = result_i[1], result_l[1]
                    y_i, y_l = result_i[2], result_l[2]
                    
                    dist = math.sqrt(((x_i-x_l) * x_scale)**2 + ((y_i - y_l) * y_scale)**2)
                    dist_matrix[i][l].append(dist)
                    
                    
        for i, row in enumerate(dist_matrix):
            for l, col in enumerate(row):
                dist_matrix[i][l] = numpy.mean(col)
        print(dist_matrix)
        
        output_file = open('Data\\MultiCompare_{:03d}.dat'.format(pID), 'w')
        for row in dist_matrix:
            for col in row:
                output_file.write('{:.3f}\t'.format(col))
            output_file.write('\n')
            
        output_file.close()

            
class PairComparisonTrial(object):
    def __init__(self, stimulus_index):
        self.stimulus_index = stimulus_index
    
    def setupStimulus(self, stimulus_pool):
        self.stimulus = [stimulus_pool[stimulus_index] for stimulus_index in self.stimulus_index]
         
    def _resetStimulusPosition(self, display):
        for i, stimulus in enumerate(self.stimulus):
            stimulus.x = int(display.w / 2 + (i*2-1) * display.w/6)
            stimulus.y = int(display.h / 2)
            
    def setupScaleCandidates(self, scale_candidates):
        self.scale_candidates = scale_candidates
            
    def run(self, display, recorder):
        self._resetStimulusPosition(display)
        display.clear(True)
        display.wait(1000)
        self._getResponse(display, recorder)
        
    def _getResponse(self, display, recorder):
        catching = True
        while catching:
            mouse_overed_scale = None
            display.clear(False)
            mouse_x, mouse_y, button = recorder.getMouse()
            
            for stimulus in self.stimulus:
                stimulus.draw(display)
                
            for scale_candidate in self.scale_candidates:
                if scale_candidate.isMouseOver(mouse_x, mouse_y):
                    mouse_overed_scale = scale_candidate
                scale_candidate.draw(display, scale_candidate.isMouseOver(mouse_x, mouse_y))
                
            if button == 'left_down' and mouse_overed_scale is not None:
                self.response = mouse_overed_scale.scale
                catching = False
                            
            display.waitFPS()
            display.refresh()
            
class PairComparison(ExperimentSession):
    def run(self):
        print(len(self.trials))
        for trial in self.trials:
            trial.setupStimulus(self.stimulus)
            trial.setupScaleCandidates(self.scale_candidates)
            trial.run(self.display, self.recorder)
        
    def constructTrials(self):
        super(PairComparison, self).constructTrials()
        self._setupScaleCandidates()
        
    def _determiningStimulusCombination(self):
        self.trials = []
        pairs = list(itertools.combinations(range(self.exp_parameters.n_items), 2))
        pairs = numpy.random.permutation(pairs)
        
        for pair in pairs:
            self.trials.append(PairComparisonTrial(numpy.random.permutation(pair)))
            
    def _setupScaleCandidates(self):
        self.scale_candidates = [Stimulus.ScaleCandidate(i+1) for i in range(9)]
        for scale_candidate in self.scale_candidates:
            scale_candidate.updateRect(self.display)
            
    def save(self, pID):
        dist_matrix = numpy.zeros((self.exp_parameters.n_items, self.exp_parameters.n_items))
        for trial in self.trials:
            dist_matrix[trial.stimulus_index[0]][trial.stimulus_index[1]] = trial.response
            dist_matrix[trial.stimulus_index[1]][trial.stimulus_index[0]] = trial.response
            
        output_file = open('Data\\PairWise_{:03d}.dat'.format(pID), 'w')
        for row in dist_matrix:
            for col in row:
                output_file.write('{:.3f}\t'.format(col))
            output_file.write('\n')
            
        output_file.close()
     
    
class Experiment(object):
    def __init__(self):
        self.exp_parameters = ExpParameters()
        self.RESOURCES = sdl2.ext.Resources('.', 'resources')
        self.display = Display.Display(self.RESOURCES, self.exp_parameters)
        self.recorder = Recorder.Recorder(self.exp_parameters)
        
        self.pID = 999
        
        self._setupSessions()
        
    def _setupSessions(self):
        self.multi_comparison_session = MultiComparison(self.exp_parameters, self.display, self.recorder, self.RESOURCES)
        self.multi_comparison_session.constructTrials()
        
        self.pair_comparison_session = PairComparison(self.exp_parameters, self.display, self.recorder, self.RESOURCES)
        self.pair_comparison_session.constructTrials()
        
    def run(self):
        self.multi_comparison_session.run()
        self.pair_comparison_session.run()
    
    def save(self):
        self.multi_comparison_session.save(self.pID)
        self.pair_comparison_session.save(self.pID)
    
    
def _main():
    exp = Experiment()
    exp.run()
    exp.save()
    pass
    

if __name__ == '__main__':
    _main()