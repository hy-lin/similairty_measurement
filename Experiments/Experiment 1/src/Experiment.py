'''
Created on 26.09.2016

@author: Hsuan-Yu Lin
'''
import itertools
import numpy.random

class ExpParameters(object):
    '''
    The experiment settings.
    '''
    
    def __init__(self):
        
        self.n_items = 10
        self.items_per_multicomparison = 4
        
        pass

class MultiComparisonTrials(object):
    def __init__(self, stimulus_index):
        self.stimulus_index = stimulus_index

class MultiComparison(object):
    '''
    The main class for the MultiComparison session of the experiment
    '''


    def __init__(self, exp_parameters):
        '''
        Constructor
        '''
        self.exp_parameters = exp_parameters
        
    def constructTrials(self):
        self.trials = []
        self._determiningStimulusCombination()
        
    def _determiningStimulusCombination(self):
        subgroup_size = int(self.exp_parameters.items_per_multicomparison / 2)
        n_subgroups = int(self.exp_parameters.n_items / subgroup_size)
        
        stimulus_pool = numpy.random.permutation(self.exp_parameters.n_items)
        subgroups = []
        for subgroup_index in range(n_subgroups):
            subgroups.append([stimulus_pool[i] for i in range(subgroup_index*subgroup_size, (subgroup_index+1)*subgroup_size)])
        
#         subgroups = [list(range(subgroup_size*i, subgroup_size*(i+1))) for i in range(n_subgroups)]
        trial_by_subgroup = list(itertools.combinations(range(n_subgroups), 2))
        for trial, subgroup in enumerate(trial_by_subgroup):
            stimulus_index = subgroups[subgroup[0]] + subgroups[subgroup[1]]
            self.trials.append(MultiComparisonTrials(stimulus_index))
            

def _main():
    exp_parameters = ExpParameters()
    multi_comparison_session = MultiComparison(exp_parameters)
    multi_comparison_session.constructTrials()

if __name__ == '__main__':
    _main()