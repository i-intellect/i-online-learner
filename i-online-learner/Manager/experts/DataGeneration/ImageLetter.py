# -*- coding: utf-8 -*-
import copy

from PIL import Image, ImageDraw, ImageFont, ImageChops
import numpy as np
import math
from scipy.misc import toimage

class ImageLetter:
    image = None #обЪект pil картинка с полотном 
    width = None #ширина полотна
    height= None #высота полотна
    fontSize = None #рзмер шрифка задаетмся в поинтах
    textImg = None #картинка только буквы без полотна
    letterImgSize = None #размер буквы без полотна
    letters = []#массив для обучение сдвиги
    lettersVector = []#массив для векторов обученяи сдвиги
    kozStep = 1#шаг сдвига
    color = (256, 256, 256)#цвет
    kostil = -5
    numberOfAddNose = 5

    def __init__(self, text, fontSize, maxSize):
        #self.height = (fontSize * 2 ** (1/2) )+fontSize
        
        fontFile = "arial.ttf" #windows /arial.ttf, #mac /Helvetica.dfont, #linux FreeMono.ttf
        fnt = ImageFont.truetype(fontFile, size=fontSize) #создаем шрифт для рисования букры
        '''
        letterSize = fnt.getsize(text)#получаем рамер прямоугольника описывающего букву
        
        maxSize = 6#max(letterSize) #находим масимальную сторну
        '''
        self.height =int(math.ceil(maxSize * (pow(2 , 0.5))))+2  #расчиваем размер полотна
        self.width = self.height#расчиваем размер полотна 
        self.fontSize = fontSize
        #self.letterImgSize = (fontSize * 2 ** (1/2), fontSize * 2 ** (1/2))
        self.letterImgSize = (maxSize, maxSize) #размер каритини с буквой без полотна
        
                             
        #рисуем картинку на полотне
        '''
        img = Image.new('RGBA', (self.width, self.height), self.color)
        imgADraw = ImageDraw.Draw(img)
        imgADraw.text(((self.width/2)-(maxSize/2), (self.height/2)-(maxSize/2)), text, font=fnt, fill=(0, 0, 0))
        #imgADraw.text((0, 0), text, font=fnt, fill=(0, 0, 0))
        self.image = img
        '''
        #generate textImg
        #создаем катинку размера буквы
        img = Image.new('RGBA', self.letterImgSize, self.color) 
        imgADraw = ImageDraw.Draw(img)
        imgADraw.text((0, self.kostil), text, font=fnt, fill=(0, 0, 0))
        img.resize((maxSize, maxSize)) #делаем ее квадраной
        self.textImg = img
        #self.textImg.show()
        
        imgB = Image.new('RGBA', (self.width, self.height), self.color)
        imgB.paste(self.textImg, ((self.width/2)-(self.letterImgSize[0]/2), (self.height/2)-(self.letterImgSize[0]/2))) 
        self.image = imgB
        self.generateAllOfset(self.kozStep) #создаем сдвиги
        
    #метод не вносит вклад в логику программы     
    def setOfset(self, steps):
        self.image = ImageChops.offset(self.image, steps[0], steps[1])
        self.generateAllOfset(self.kozStep)
        return self
    
    #метод  создает полотно помещает картинку букрвы в координаты, сохранеет картинку и вектор
    def setLetterOfset(self, x, y):
        imgB = Image.new('RGBA', (self.width, self.height), self.color)#создаем полотно
        imgB.paste(self.textImg, (x, y), self.textImg) #вставляем картинку буквы

        vector = np.array(list(imgB.getdata(band=1)))
        vector[vector <= 255 / 2 ] = 1.0
        vector[vector > 255 / 2 ] = 0.0
        self.letters.append(imgB) #сохраняем картунку
        self.lettersVector.append(vector) #сохраняем вектор
        self.addNoise(vector)

    def addNoise(self, vectorOrig):
        for j in range(0, self.numberOfAddNose):
            vector = copy.deepcopy(vectorOrig)
            for i in range(0, len(vector)):
                rnd = np.random.random()
                if (rnd >= 0.99) :
                    vector[i] = float(not bool(vector[i]))
            self.lettersVector.append(vector)
            w = h = int(math.sqrt(len(vector)))
            vectorT = 1.0 - vector
            data =  vectorT.reshape(h, w)
            toimage(data).save(r"C:\\img\noise\\" + str(rnd) + ".jpg")
            #img = toimage(data,mode='RGBA')
            # self.letters.append(img)

    #метод для вращения картинки
    def setRotate(self, step):
        #img = Image.new('RGBA', self.letterImgSize, self.color) #создаем фрэйм для картиники буквы 
        #img = Image.new('RGBA', (self.width, self.height), self.color)
        imgB = Image.new('RGBA', (self.width, self.height), self.color) #создаем полотно
        textImgR =self.textImg.rotate(step, resample=Image.BILINEAR, expand = 1 )#povorot
        # textImgR.show()
        self.textImg = textImgR# Image.composite(textImgR, img, textImgR) # вставляем картинку на фрэм
        #self.textImg.show()
        imgB.paste(self.textImg, ((self.width/2)-(self.letterImgSize[0]/2)-5, (self.height/2)-(self.letterImgSize[0]/2)-2),self.textImg) #вставляем букрву на полотно
        self.image = imgB
        self.generateAllOfset(self.kozStep)#созадем данные для обучения с шагом 
        
        return self
    #масштабируем картинку 
    def setResize(self, step):
        img = Image.new('RGBA', self.letterImgSize, self.color) #создаем фрэйм для картиники буквы 
        imgB = Image.new('RGBA', (self.width, self.height), self.color) #создаем полотно
        imgResize = self.textImg.resize((self.letterImgSize[0] - (step ), self.letterImgSize[1] - (step))) #ресайзем картинку
        self.letterImgSize = (self.letterImgSize[0] - (step ), self.letterImgSize[1] - (step))
        self.textImg = imgResize
        #img.paste(imgResize, ((self.width/2 - (self.width - (step * 16))/2), (self.height/2 - (self.height - (step * 9))/2)))
        imgB.paste(imgResize, ((self.width/2)-(self.letterImgSize[0]/2), (self.height/2)-(self.letterImgSize[0]/2)), imgResize)#вставляем букрву на полотно
        self.image = imgB
        self.generateAllOfset(self.kozStep)#созадем данные для обучения с шагом 
        return self

    #метод преобразования в лист
    def getRaw(self):
        return list(self.image.getdata(band=1))

    #метод возвращает картинки в векторе
    def getVector(self):
        # vector = np.array(list(self.textImg.getdata(band=1)))
        # vector[vector <= 255 / 2 ] = 1.0
        # vector[vector > 255 / 2 ] = 0.0
        return self.lettersVector[0]

    #делаем смещение с шагом
    def generateAllOfset(self, step):
        self.letters = []
        self.lettersVector = []
        '''
        for x in range(0, (self.width - self.letterImgSize[0]) - step, step):
            for y in range(0, (self.height -self.letterImgSize[1]) - step , step):
                self.setLetterOfset(x, y)
        '''
        '''
        self.setLetterOfset(2, 2)
        self.setLetterOfset(1, 2)
        self.setLetterOfset(2, 1)
        self.setLetterOfset(3, 2)
        self.setLetterOfset(2, 3)
        '''
        self.addImgCenter()
        for x in range((self.width/2)-(self.letterImgSize[0]/2)-1,(self.width/2)-(self.letterImgSize[0]/2) + 1, step): 
            for y in range((self.width/2)-(self.letterImgSize[0]/2)-1,(self.height/2)-(self.letterImgSize[1]/2) + 1  , step):
                self.setLetterOfset(x, y)

    #добавляем картинку с буквой в центре к смещенным буквам
    def addImgCenter(self):                
        vector = np.array(list(self.image.getdata(band=1)))
        vector[vector <= 255 / 2 ] = 1.0
        vector[vector > 255 / 2 ] = 0.0
        
        self.letters.append(self.image)
        self.lettersVector.append(vector) #сохраняем вектор
