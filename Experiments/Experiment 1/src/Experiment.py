'''
Created on 26.09.2016

@author: Hsuan-Yu Lin
'''
import itertools

class ExpParameters(object):
    '''
    The experiment settings.
    '''
    
    def __init__(self):
        
        self.n_items = 10
        self.items_per_multicomparison = 4
        
        pass



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
        
    def determiningStimulusCombination(self):
        subgroup_size = self.exp_parameters.items_per_multicomparison / 2
        n_subgroups = self.exp_parameters.n_items / subgroup_size
        
        subgroups = [list(range(subgroup_size*i, subgroup_size*(i+1))) for i in range(n_subgroups)]
        trial_by_subgroup = list(itertools.combinations(range(n_subgroups), 2))