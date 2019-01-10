# -*- coding: utf-8 -*-
"""
Created on Wed May 10 11:16:25 2017

@author: valekseev, puchkoff
"""
from scipy.misc import toimage

import numpy as np
#import math 

np.set_printoptions(threshold=np.nan)
class Expert:
    letter1 = None
    letter2 = None
    weight = None
    answers = None
    probability = None
    lastResult = None
    W = None
    #стартовое значение для a
    a=0.001
    #увеличение a через количество эпох
    numberOfEpochs = 50

    def __init__(self, vectorA, vectorB):
        self.weight = []
        self.answers = []
        self.probability = []
        self.lastResult = 0
        self.weight.append(1)
        self.letter1 = vectorA
        self.letter2 = vectorB

        Z = []
        A = []
        #Вычисляем все вектора Z
        for positionA in vectorA:
            for positionB in vectorB:
                raznost = positionA - positionB
                Z.append(raznost)
                A.append(pow((np.sum(pow(raznost, 2))), 0.5))
        aNp = np.array(A)
        aMinIndex =aNp.argmin()

        # arr = vectorB[0].reshape(34, 34)
        # toimage(arr).show()
        # arr = vectorB[1].reshape(34, 34)
        # toimage(arr).show()
        # arr = vectorB[2].reshape(34, 34)
        # toimage(arr).show()
        # arr = vectorB[3].reshape(34, 34)
        # toimage(arr).show()

        self.W = Z[aMinIndex]
        aMax = 1
        
        WArray= []
        WAmaxArray = []
        epochs=self.numberOfEpochs

        #Настраиваем веса
        while aMax > self.a:
        #for i in range(0, self.numberOfEpochs):
            aArray = []
            for z in range(0, len(Z) - 1):
                if (np.array_equal(Z[z], self.W) == False):# aMinIndex != z :
                    aArray.append(float(np.dot(self.W, (self.W - Z[z]))) /float(np.dot((self.W - Z[z]) , (self.W - Z[z]))))

            aNp = np.array(aArray)
            aMaxIndex = aNp.argmax()
            aMax = aNp.max()
            #print '--------', aMax
            WAmaxArray.append(aMax)
            WArray.append(self.W)
            self.W = self.W + aMax * (Z[aMaxIndex] - self.W)
            epochs-=1
            
            if epochs==0:
                epochs=self.numberOfEpochs
                self.a+=0.001
        A = []
        B = []


        # aNp = np.array(WAmaxArray)
        # aMax-MinIndex = aNp.argmin()
        # #print '--------', aNp.min()
        # self.W = WArray[aMaxMinIndex]

        #Рассчитать порог
        for positionA in vectorA:
            A.append(np.dot(positionA , self.W))
        a = np.array(A)
        aMin  = a.min()
        for positionB in vectorB:
            B.append(np.dot(positionB , self.W))
        b = np.array(B)
        bMax  = b.max()
        
        self.Q = (aMin + bMax) / 2

       # self.Q = bMax + pow(np.dot(self.W , self.W), 0.5)/2



        
    def predict(self, vector):

        #arr = vector.reshape(30, 30)
        #toimage(arr).show()

        v = np.dot(vector, self.W)
        #print (v, self.Q)
        if v >= self.Q:
            self.lastResult = 0
        else:
            self.lastResult = 1

    def __str__(self):

        weight = ''.join(str(self.weight[len(self.weight)-1]))
        if (len(self.answers)> 0):
            answers = ''.join(str(self.answers.count(True)/float(len(self.answers))))
        else:
            answers = ''
        probability = ''.join(str(self.probability[len(self.probability)-1]))
        return ''.join([ 'weight : ', weight, '\n --- \n', 'answers : ', answers, '\n --- \n', 'probablity : ', probability, ' \n-----------------'])
        