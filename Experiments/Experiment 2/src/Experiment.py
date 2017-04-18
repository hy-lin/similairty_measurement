# coding= latin-1
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
import datetime

class ExpParameters(object):
    '''
    The experiment settings.
    '''
    
    def __init__(self):
        
        self.n_items = 16
        self.items_per_multicomparison = 8
        self.n_repetition = 2
        self.max_rating = 9
        
        self.n_practice_items = 16
        self.n_multi_compare_practice_trials = 2
        self.n_pair_compare_practice_trials = 4
        
        self.n_break = 10
        
        self.font_size = 36
        
        pass

class MultiComparisonTrials(object):
    def __init__(self, stimulus_index):
        self.stimulus_index = stimulus_index
        self.stimulus = []
        
    def setupStimulus(self, stimulus_pool):
        self.stimulus = list(range(len(self.stimulus_index)))
        for i, stimulus_index in enumerate(self.stimulus_index):
            self.stimulus[i] = stimulus_pool[stimulus_index]
            
    def run(self, display, recorder):
        self._resetStimulusPosition(display)
        
        st = recorder.getTicks()
        
        display.wait(300)
        self._getResponse(display, recorder)
        self._recordResponse()
        
        self.t = recorder.getTicks() - st
        
        display.clear(True)
        display.wait(1000)
        
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
        st = recorder.getTicks()
        self._resetStimulusPosition(display)
        self._getResponse(display, recorder)
        display.clear(True)
        self.t = recorder.getTicks() - st
        display.wait(1000)
        
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
            
class ExperimentSession(object):
    def __init__(self, exp_parameters, display, recorder, RESOURCES):
        '''
        Constructor
        '''
        self.exp_parameters = exp_parameters
        
        self.display = display
        self.recorder = recorder
        self.RESOURCES = RESOURCES
        
        self.faces_surface = sdl2.ext.load_image(self.RESOURCES.get_path('faces_small.png'))
        
        self.logger = open('Data\\log.dat', 'a')
        self.log('Session initiated.')
        
    def constructTrials(self):
        self.practice_trials = []
        self._constructPracticeTrials()
        self.log('Practice trial constructed')
        
        self.trials = []
        self._constructTrials()
        self.log('Experiment trial constructed')
        
        self._setupPracticeSurface()
        self._setupStimulusSurface()
        
    def _beginPracticeTrialMessage(self):
        self.log('Practice session begins')
        
        self.display.clear()
        self.display.drawText(u'Mit Leertaste weiter zu den Übungsaufgaben', font_size=self.exp_parameters.font_size)
        self.display.refresh()
        self.recorder.recordKeyboard(['space'])
        
    def _beginExperimentTrialMessage(self):
        self.log('Test session begins')
        
        self.display.clear()
        self.display.drawText(u'Mit Leertaste weiter zu den Testaufgaben', font_size=self.exp_parameters.font_size)
        self.display.refresh()
        self.recorder.recordKeyboard(['space'])
        self.display.clear(refresh = True)
        
    def _endSessionMessage(self):
        self.log('Session ended')
        
        self.display.clear()
        self.display.drawText(u'Ende des Session: Bitte Versuchsleiter rufen', font_size=self.exp_parameters.font_size)
        self.display.refresh()
        self.recorder.recordKeyboard([b'K'])
        
    def _endExperimentMessage(self):
        self.log('Session ended')
        
        self.display.clear()
        self.display.drawText(u'Ende des Experiments: Bitte Versuchsleiter rufen', font_size=self.exp_parameters.font_size)
        self.display.refresh()
        self.recorder.recordKeyboard(['space'])
        
    def _takingBreak(self):
        self.log('Taking a break')
        
        self.display.clear()
        self.display.drawText(u'Gelegenheit für kurze Pause. Weiter mit Leertaste', font_size=self.exp_parameters.font_size)
        self.display.refresh()
        self.recorder.recordKeyboard(['space'])
        self.display.clear(refresh = True)
        
    def _constructPracticeTrials(self):
        print('If you see this, I fucked up. Please inform experimenter.')
        raise NameError('Function: _constructPracticeTrials is not defined in class: ExperimentSession')
    
    def _constructTrials(self):
        print('If you see this, I fucked up. Please inform experimenter.')
        raise NameError('Function: _constructTrials is not defined in class: ExperimentSession')
        
    def _setupStimulusSurface(self):
        self.stimulus = []
        
        Lab_center = Stimulus.Color_Lab(70.0, 20.0, 38.0)
        colors = [Stimulus.angle2RGB(ang, Lab_center, 60.0) for ang in numpy.linspace(0, 360, self.exp_parameters.n_items + 1)]
        
        for i in range(self.exp_parameters.n_items):
            self.stimulus.append(Stimulus.ColorPatch(colors[i], -1, -1, i))
            
            self.stimulus[i].updateStimulusSurface()
            
    def _setupPracticeSurface(self):
        self.practice_stimulus_pool = []
        
        for i in range(self.exp_parameters.n_practice_items):
            i_binary = '{0:04b}'.format(i)
            eyes_gap = int(i_binary[0]) * 2 + 1
            eyes_position = int(i_binary[1]) * 2 + 1
            nose_length = int(i_binary[2]) * 2 + 1
            mouth_position = int(i_binary[3]) * 2 + 1
            self.practice_stimulus_pool.append(Stimulus.ReedFace([eyes_gap, eyes_position, nose_length, mouth_position], -1, -1, i))
            
            self.practice_stimulus_pool[i].updateStimulusSurface(self.faces_surface)
            
            
    def log(self, msg):
        current_time = datetime.datetime.now()
        time_str = current_time.strftime('%d-%b-%Y %I-%M-%S')
        
        output_string = '{}\t{}'.format(time_str, msg)
        print(output_string)
        self.logger.write('{}\n'.format(output_string))

class MultiComparison(ExperimentSession):
    '''
    The main class for the MultiComparison session of the experiment
    '''

    def run(self):
        self.log('Multi-item arrangement session starts')
        
        self._beginPracticeTrialMessage()
        
        for i, practice_trial in enumerate(self.practice_trials):
            self.log('practice trial {} begins'.format(i))
            
            practice_trial.setupStimulus(self.practice_stimulus_pool)
            practice_trial.run(self.display, self.recorder)
            
            self.log('practice trial {} end'.format(i))
        
        self._beginExperimentTrialMessage()
        
        for i, trial in enumerate(self.trials):
            self.log('test trial {} begins'.format(i))
            
            trial.setupStimulus(self.stimulus)
            trial.run(self.display, self.recorder)
            
            self.log('test trial {} end'.format(i))
            
        self._endSessionMessage()
            
    def _constructPracticeTrials(self):
        self.log('constructing practice trials begins')
        
        for i in range(self.exp_parameters.n_multi_compare_practice_trials):
            item_indexes = numpy.random.permutation(self.exp_parameters.n_practice_items)
            stimulus_index = [item_indexes[i] for i in range(self.exp_parameters.items_per_multicomparison)]
            self.practice_trials.append(MultiComparisonTrials(stimulus_index))
            
        self.log('constructing practice trials end')

    def _constructTrials(self):
        self.log('constructing test trials begins')
        
        subgroup_size = int(self.exp_parameters.items_per_multicomparison / 2)
        n_subgroups = int(self.exp_parameters.n_items / subgroup_size)
        
        subgroups = []
        for i in range(self.exp_parameters.n_repetition):
            stimulus_pool = numpy.random.permutation(self.exp_parameters.n_items)
            
            for subgroup_index in range(n_subgroups):
                subgroups.append([stimulus_pool[i] for i in range(subgroup_index*subgroup_size, (subgroup_index+1)*subgroup_size)])
            
            trial_by_subgroup = itertools.combinations(range(n_subgroups), 2)
            for subgroup in trial_by_subgroup:
                stimulus_index = subgroups[subgroup[0]] + subgroups[subgroup[1]]
                self.trials.append(MultiComparisonTrials(stimulus_index))
                
        self.log('constructing test trials end')
                
    def save(self, pID, session):
        self.log('saving starts')
        
        self._saveSimilarityMatrix(pID, session)
        self._saveTrial(pID, session)
        
        self.log('saving finished. WE GOOD. maybe.')
        self.logger.close()
        
    def _saveSimilarityMatrix(self, pID, session):
        dist_matrix = [[[]for m in range(self.exp_parameters.n_items)] for n in range(self.exp_parameters.n_items)]
        
        min_x, min_y, max_x, max_y = 9999, 9999, -9999, -9999
        for trial in self.trials:
            t_min_x, t_min_y, t_max_x, t_max_y = trial.findResponseMinMax()
            
            if t_min_x <= min_x:
                min_x = t_min_x
            if t_min_y <= min_y:
                min_y = t_min_y
            if t_max_x >= max_x:
                max_x = t_max_x
            if t_max_y >= max_y:
                max_y = t_max_y

        x_scale = 1280.0/(max_x - min_x)
        y_scale = 1024.0/(max_y - min_y)
        
        print(x_scale, y_scale)
        
        for trial in self.trials:
            for result_i in trial.result:
                for result_l in trial.result:
                    i, l = result_i[0], result_l[0]
                    x_i, x_l = result_i[1], result_l[1]
                    y_i, y_l = result_i[2], result_l[2]
                    
                    dist = math.sqrt(((x_i-x_l) * x_scale)**2 + ((y_i - y_l) * y_scale)**2)
                    
                    print(i, x_i, x_l, l, y_i, y_l, dist)
                    
                    dist_matrix[i][l].append(dist)
                    
                    
        for i, row in enumerate(dist_matrix):
            for l, col in enumerate(row):
                dist_matrix[i][l] = numpy.mean(col)
        
        output_file = open('Data\\SimilarityMatrix\\MultiItemsArrangement_{:03d}_{:02d}.dat'.format(pID, session), 'a')
        for row in dist_matrix:
            for col in row:
                output_file.write('{:.3f}\t'.format(col))
            output_file.write('\n')
            
        output_file.close()

    def _saveTrial(self, pID, session):
        output_file = open('Data\\TrialsDetail\\MultiItemsArrangement_{:03d}_{:02d}.dat'.format(pID, session), 'a')
        for i, trial in enumerate(self.trials):
            output_file.write('{:d}\t'.format(i))
            for result in trial.result:
                output_file.write('{:d}\t{:d}\t{:d}\t'.format(result[0], result[1], result[2]))
                
            output_file.write('{:d}\t'.format(trial.t))
            output_file.write('\n')
            
        output_file.close()
            
class PairComparison(ExperimentSession):
    def run(self):
        self.log('Pair comparison session starts')

        self._beginPracticeTrialMessage()
        for i, practice_trial in enumerate(self.practice_trials):
            self.log('Practice trial {} begins'.format(i))
            
            practice_trial.setupStimulus(self.practice_stimulus_pool)
            practice_trial.setupScaleCandidates(self.scale_candidates)
            practice_trial.run(self.display, self.recorder)
            
            self.log('Practice trial {} end'.format(i))

        self._beginExperimentTrialMessage()
        for i, trial in enumerate(self.trials):
            self.log('Test trial {} begins'.format(i))
            
            trial.setupStimulus(self.stimulus)
            trial.setupScaleCandidates(self.scale_candidates)
            trial.run(self.display, self.recorder)
            
            self.log('Test trial {} end'.format(i))
            
            if i != 0 and i % int(len(self.trials)/self.exp_parameters.n_break) == 0:
                self._takingBreak()
            
        self._endExperimentMessage()
        
    def constructTrials(self):
        super(PairComparison, self).constructTrials()
        self._setupScaleCandidates()
        
    def _constructPracticeTrials(self):
        self.log('constructing practice trials begins')
        
        for i in range(self.exp_parameters.n_pair_compare_practice_trials):
            item_indexes = numpy.random.permutation(self.exp_parameters.n_practice_items)
            stimulus_index = [item_indexes[i] for i in range(2)]
            self.practice_trials.append(PairComparisonTrial(stimulus_index))
            
        self.log('constructing practice trials end')
        
    def _constructTrials(self):
        self.log('constructing test trials begins')

        self.trials = []
        pairs = list(itertools.combinations(range(self.exp_parameters.n_items), 2))
        pairs = pairs * self.exp_parameters.n_repetition
        pairs = numpy.random.permutation(pairs)
        
        for pair in pairs:
            self.trials.append(PairComparisonTrial(numpy.random.permutation(pair)))
            
        self.log('constructing test trials end')
            
    def _setupScaleCandidates(self):
        self.scale_candidates = [Stimulus.ScaleCandidate(i+1) for i in range(self.exp_parameters.max_rating)]
        for scale_candidate in self.scale_candidates:
            scale_candidate.updateRect(self.display)
            
    def save(self, pID, session):
        self.log('saving starts')

        self._saveSimilarityMatrix(pID, session)
        self._saveTrial(pID, session)
        
        self.log('saving finished. WE GOOD. maybe.')
        self.logger.close()
        
    def _saveSimilarityMatrix(self, pID, session):
        dist_matrix = [[[]for m in range(self.exp_parameters.n_items)] for n in range(self.exp_parameters.n_items)]
        
        for trial in self.trials:
            dist = self.exp_parameters.max_rating - trial.response
            dist_matrix[trial.stimulus_index[0]][trial.stimulus_index[1]].append(dist)
            dist_matrix[trial.stimulus_index[1]][trial.stimulus_index[0]].append(dist)
            
        output_file = open('Data\\SimilarityMatrix\\PairWise_{:03d}_{:02d}.dat'.format(pID, session), 'a')
        for row in dist_matrix:
            for col in row:
                if col:
                    output_file.write('{:.3f}\t'.format(numpy.mean(col)))
                else:
                    output_file.write('{:.3f}\t'.format(0.0))
            output_file.write('\n')
            
        output_file.close()
        
    def _saveTrial(self, pID, session):
        output_file = open('Data\\TrialsDetail\\PairWise_{:03d}_{:02d}.dat'.format(pID, session), 'a')
        for i, trial in enumerate(self.trials):
            output_file.write('{:d}\t'.format(i))
            output_file.write('{:d}\t{:d}\t{:d}\t'.format(trial.stimulus_index[0], trial.stimulus_index[1], trial.response))
            output_file.write('{:d}\t'.format(trial.t))
            output_file.write('\n')

        output_file.close()
    
class Experiment(object):
    def __init__(self):
        self.exp_parameters = ExpParameters()
        self.RESOURCES = sdl2.ext.Resources('.', 'resources')
        self.display = Display.Display(self.RESOURCES, self.exp_parameters)
        self.recorder = Recorder.Recorder(self.exp_parameters)
        
        self.pID = 999
        self.session = 99
        
        self._setupSessions()
        self._getPIDNSession()
        
    def _setupSessions(self):
        self.multi_comparison_session = MultiComparison(self.exp_parameters, self.display, self.recorder, self.RESOURCES)
        self.multi_comparison_session.constructTrials()
        
        self.pair_comparison_session = PairComparison(self.exp_parameters, self.display, self.recorder, self.RESOURCES)
        self.pair_comparison_session.constructTrials()
    
    def _getPIDNSession(self):
        pID = self.display.getString(self.recorder, 'Participant ID: ', 20, 20)
        session = self.display.getString(self.recorder, 'Session: ', 20, 20)
        
        self.pID = int(pID)
        self.session = int(session)
    
    def run(self):
        self.multi_comparison_session.run()
        self.multi_comparison_session.save(self.pID, self.session)

        self.pair_comparison_session.run()
        self.pair_comparison_session.save(self.pID, self.session)

def _main():
    exp = Experiment()
    exp.run()
    pass
    

if __name__ == '__main__':
    _main()