'''
Created on 17.10.2016

@author: Hsuan-Yu Lin
'''
import numpy
import math
import sklearn.manifold
import matplotlib.pyplot as plt

def _setupStimulus():
    stimulus = [[222.0/255.0, 225.0/255.0, 255.0/255.0], \
                [190.0/255.0, 234.0/255.0, 253.0/255.0], \
                [115.0/255.0, 114.0/255.0, 168.0/255.0], \
                [110.0/255.0, 153.0/255.0, 186.0/255.0], \
                [62.0/255.0, 122.0/255.0, 168.0/255.0], \
                [38.0/255.0, 122.0/255.0, 161.0/255.0]]
    
    return stimulus

def _dist(items):
    dist_array = numpy.zeros((len(items), len(items)))
    for i, item_i in enumerate(items):
        for l, item_l in enumerate(items):
            print([(item_i[d] - item_l[d])**2 for d in range(len(item_i))])
            dist_array[i, l] = math.sqrt(sum([(item_i[d] - item_l[d])**2 for d in range(len(item_i))]))
            
    return dist_array

def mdsTest():
    model = sklearn.manifold.MDS(max_iter = 1000000, eps = 1e-10, dissimilarity='precomputed')
    
    stimulus = _setupStimulus()
    dist_array = _dist(stimulus)
    print(dist_array)
    model.fit(dist_array)
    print(model.embedding_)
    print(model.stress_)
    
    for i, s in enumerate(stimulus):
        plt.text(model.embedding_[i, 0], model.embedding_[i, 1], str(i))
        print(str(i))
#     plt.scatter(model.embedding_[:, 0], model.embedding_[:, 1], c = stimulus)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.show()
    
    pass

if __name__ == '__main__':
    mdsTest()
    pass