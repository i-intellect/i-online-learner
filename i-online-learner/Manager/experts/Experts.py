# -*- coding: utf-8 -*-
from Expert import Expert
import math
from scipy.misc import toimage

class Experts:
    experts = []
    def __init__(self, dataset):

        for items in range(1,len(dataset[0])):
            ex = Expert(dataset[0][items].lettersVector, dataset[1][items].lettersVector)
            ex.predict(dataset[0][items].lettersVector[3])
            #print ex.lastResult
            ex.predict(dataset[1][items].lettersVector[3])
            #print ex.lastResult
            ex.probability.append(1/float(len(dataset[0])))
            # h=w=int(math.sqrt(len(dataset[0][items].lettersVector[3])))
            # arr = dataset[0][items].lettersVector[3].reshape(h, w)
            # toimage(arr).show()
            self.experts.append(ex)


        for i in range(1, len(dataset[0])):
            j = 0
            for e in self.experts:
                j += 1
                # h=w=int(math.sqrt(len(dataset[0][i].lettersVector[3])))
                # arr = dataset[0][i].lettersVector[3].reshape(h, w)
                # toimage(arr).show()
                #e.predict(dataset[0][i].lettersVector[6])
                #print 'На букву А из ', i , ' выборки  эксперт №', j, ' ответил ', e.lastResult

    def getList(self):
        return self.experts