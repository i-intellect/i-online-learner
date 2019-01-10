# -*- coding: utf-8 -*-
from PIL import ImageFont
from ImageLetter import ImageLetter
import copy
import numpy as np
import math
from scipy.misc import toimage

class Dataset:
    
    rotateSteps = None
    ofsetSteps = None
    resizeStep = None
    resizeValue = None
    fontSize = 30
    text1 = "A"
    text2 = "B"
    imgPath = r"C:\\img"
    data = [[], []]
    maxSize = None
    #Построение обучающих выборок
    def __init__(self, ofsetSteps, resizeStep, resizeValue, rotateSteps):
        
        self.rotateSteps = rotateSteps
        self.ofsetSteps = 1
        self.resizeStep = resizeStep
        self.resizeValue = resizeValue
        size = self.getSizeOfFontSize()
        #1 буква
        #for i in range(0, ofsetSteps, 1):
        img = ImageLetter(self.text1, self.fontSize, size)
        #img.image.show()
        #img = img.setOfset((0, ofsetSteps * i))
        self.data[0].append([img, []])
        '''
        for j in range(0, ofsetSteps, 1):
            img = ImageLetter(self.text1, self.fontSize, size)
            img = img.setOfset((ofsetSteps * j, ofsetSteps * i))
            self.data[0].append([img, []])
        '''

        for i in range(0,len(self.data[0])):
            for r in range((300 / rotateSteps -1), 300 , (300 / rotateSteps - 1)):
                imgN = copy.deepcopy(self.data[0][i][0])
                imgN = imgN.setRotate(r)
                self.data[0][i][1].append([imgN,[]])

        for i in range(0,len(self.data[0])):
            for j in range(0, len(self.data[0][i][1])):
                for resize in range(resizeValue, resizeStep * resizeValue + 1, resizeValue):
                    imgN = copy.deepcopy(self.data[0][i][1][j][0])
                    imgN = imgN.setResize(resize)
                    self.data[0][i][1][j][1].append(imgN)
        #2 буква

        #for i in range(0, ofsetSteps, 1):
        img = ImageLetter(self.text2, self.fontSize, size)
        #img = img.setOfset((0, ofsetSteps * i))
        self.data[1].append([img, []])
        '''
        for j in range(0, ofsetSteps, 1):
            img = ImageLetter(self.text2, self.fontSize, size)
            img = img.setOfset((ofsetSteps * j, ofsetSteps * i))
            self.data[1].append([img, []])
        '''

        for i in range(0,len(self.data[1])):
            for r in range((300 / rotateSteps-1), 300 , (300 / rotateSteps-1)):
                imgN = copy.deepcopy(self.data[1][i][0])
                imgN = imgN.setRotate(r)
                self.data[1][i][1].append([imgN,[]])

        for i in range(0,len(self.data[1])):
            for j in range(0, len(self.data[1][i][1])):
                for resize in range(resizeValue, resizeStep * resizeValue + 1, resizeValue):
                    imgN = copy.deepcopy(self.data[1][i][1][j][0])
                    imgN = imgN.setResize(resize)
                    self.data[1][i][1][j][1].append(imgN)

    #Максимальный размер буквы в шрифте
    def getSizeOfFontSize(self):
        fontFile = "arial.ttf" #windows /arial.ttf, #mac /Helvetica.dfont, #linux FreeMono.ttf
        fnt = ImageFont.truetype(fontFile, size=self.fontSize) #создаем шрифт для рисования букры
        letterSize1 = fnt.getsize(self.text1)#получаем рамер прямоугольника описывающего букву
        fnt = ImageFont.truetype(fontFile, size=self.fontSize) #создаем шрифт для рисования букры
        letterSize2 = fnt.getsize(self.text1)#получаем рамер прямоугольника описывающего букву
        size1 = max(letterSize1)
        size2 = max(letterSize2)
        return max(size1,size2)
        
    #Примеры букв (вектора) из каждой выборки, из которых выбираются вектора для обучения менеджера
    def getData(self):
        vectors = [[],[]]
        #for img in self.data[0]:
        img = self.data[0][0]
        #vectors[0].append(self.getVector(img[0]))
        for imgR in img[1]:
            vectors[0].append(imgR[0].getVector())
            for imgT in imgR[1]:
                vectors[0].append(imgT.getVector())
        #for img in self.data[1]:
        img = self.data[1][0]
        #vectors[1].append(self.getVector(img[0]))
        for imgR in img[1]:
            vectors[1].append(imgR[0].getVector())
            for imgT in imgR[1]:
                vectors[1].append(imgT.getVector())
        # for v in vectors[0]:
        #     h = w = int(math.sqrt(len(v)))
        #     arr = v.reshape(h, w)
        #     toimage(arr).show()

        return vectors

    #Получаем все обучающие выборки для экспертов в виде векторов
    def getDataForEx(self):
        vectors = [[],[]]
        #for img in self.data[0]:
        img = self.data[0][0]
        i = 0
        j = 0
        k = 0
        img[0].image.save(self.imgPath + r"\0\1_" + str(i) + "_" + str(j)  + ".PNG" , "PNG")
        vectors[0].append(img[0])
        k = 0 
        for let in img[0].letters:
            let.save(self.imgPath + r"\0\1_" + str(i) + "_" + str(j) + "_" + str(k)  + ".PNG" , "PNG")
            k = k + 1
        for imgR in img[1]:
            i = i + 1
            imgR[0].image.save(self.imgPath + r"\0\1_" + str(i) + "_" + str(j)  + ".PNG" , "PNG")
            k = 0 
            for let in imgR[0].letters:
                let.save(self.imgPath + r"\0\1_" + str(i) + "_" + str(j) + "_" + str(k)  + ".PNG" , "PNG")
                k = k + 1
            vectors[0].append(imgR[0])
            for imgT in imgR[1]:
                j = j + 1
                imgT.image.save(self.imgPath + r"\0\1_" + str(i) + "_" + str(j)  + ".PNG" , "PNG")
                
                k = 0 
                for let in imgT.letters:
                    let.save(self.imgPath + r"\0\1_" + str(i) + "_" + str(j) + "_" + str(k)  + ".PNG" , "PNG")
                    k = k + 1
                vectors[0].append(imgT)
            j = 0
        
        #for img in self.data[1]:
        img = self.data[1][0]
        i = 0
        j = 0
        img[0].image.save(self.imgPath + r"\1\1_" + str(i) + "_" + str(j)  + ".PNG" , "PNG")
        vectors[1].append(img[0])        
        k = 0 
        for let in img[0].letters:
            let.save(self.imgPath + r"\1\1_" + str(i) + "_" + str(j) + "_" + str(k)  + ".PNG" , "PNG")
            k = k + 1
        for imgR in img[1]:
            i = i + 1
            imgR[0].image.save(self.imgPath + r"\1\1_" + str(i) + "_" + str(j)  + ".PNG" , "PNG")
            vectors[1].append(imgR[0])        
            k = 0 
            for let in imgR[0].letters:
                let.save(self.imgPath + r"\1\1_" + str(i) + "_" + str(j) + "_" + str(k)  + ".PNG" , "PNG")
                k = k + 1
            for imgT in imgR[1]:
                j = j + 1
                imgT.image.save(self.imgPath + r"\1\1_" + str(i) + "_" + str(j)  + ".PNG" , "PNG")
                vectors[1].append(imgT)
                k = 0 
                for let in imgT.letters:
                    let.save(self.imgPath + r"\1\1_" + str(i) + "_" + str(j) + "_" + str(k)  + ".PNG" , "PNG")
                    k = k + 1
            j = 0

            # for v in vectors[0]:
            #      h = w = int(math.sqrt(len(v.lettersVector[0])))
            #      arr = v.lettersVector[0].reshape(h, w)
            #      toimage(arr).show()
        return vectors

'''
np.set_printoptions(threshold=np.nan)
data= Dataset(2,1,1,3)
#data.data[0][1][1][1][0].image.show()
#print data.data[0][1][1][0][0].image.show()

#for img in data.data[0][1][1][0][0].letters:
#    img.show()

print len(data.getData()[0])

'''

