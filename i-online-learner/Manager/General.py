# coding=utf-8
from experts.DataGeneration import Dataset
from experts import Experts
from numpy import random
import numpy
import math
import pylab
import matplotlib.pyplot as plt
from terminaltables import AsciiTable

class General:
    experts = []
    nature = None
    # Kolichestvo kartinok
    count = 12
    steps = 1000
    h = 1
    results = []
    faults = []
    itogo = []
    images = [] # 0-вектор буквы А, 1-вектор буквы Б, 2-вероятность, 3-индекс, 4-эксперт

    def __init__(self, count, ofsetSteps, resizeStep, resizeValue, rotateSteps):
        """Form a complex number.

            Keyword arguments:
            count -- Count choise image
            ofsetSteps -- 
            resizeStep -- count image scale
            resizeValue -- scale size in px 
            rotateSteps -- count image rotate

            """
        # Генерируем среду
        self.nature = Dataset(ofsetSteps, resizeStep, resizeValue, rotateSteps)

        # Обучаем экспертов
        self.experts = Experts(self.nature.getDataForEx())
        #print len(self.experts.getList())
        self.count = count

    # Зупускаем обучение управляющего элемента
    def run(self):
        # Выбираем индексы картинок
        #numpy.random.seed(20)
        #numberItems = random.choice(len(self.nature.getData()[0]), size=self.count, replace=False)
        numberItems=[0,1,3,4,5,7,8,9, 11]

        # Выставляем вероятности картинок
        self.set_probablity_images(numberItems);

        i = 0
        resetH = 1
        j = 1
        while (i < self.steps):
            if (resetH == i or resetH == 1):
                resetH = resetH * 2
                j = 1
            #h = math.sqrt((8 * math.log10(len(self.experts.getList()))) / math.pow(2, j))
            h=0.5
            #print h
            image = None
            resultTrue = None
            resultManager = False

            # Выбираем случайно картинку а или b
            resultTrue= numpy.random.choice([0,1])

            # Получаем вектор картинки
            image = self.get_image(resultTrue)

            # Проходим по экспертам и подаем им картинку
            self.walk_experts(i, h, image)

            # Выбираем по веряотности экспертов ответ менелжера
            resultManager = self.choise_true_result(i)

            # Обновляем веса экспертов
            self.set_weight_experts(resultTrue)

            # Обновляем вероятности экспертов
            self.set_probablity_experts()

            # Проверям ответ менеджера с реальным ответом
            if (resultManager == resultTrue):
                self.results.append(True)
            else:
                self.results.append(False)

            # Записываем ошибку на текущем шаге
            self.faults.append(self.results.count(False)/float(len(self.results)))

            i = i + 1
            j = j + 1
        # Формируем итоговую таблицу
        self.itogo.append(['index', 'probability image', 'probability expert', 'error'])
        for image in self.images:
            self.itogo.append([image[3],
                               image[2],
                               image[4].probability[len(image[4].probability)-1],
                               image[4].answers.count(False)/float(len(image[4].answers))])
        for index in numpy.array(xrange(0,len(self.nature.getData()[0])-1)):

            if (index not in numberItems):
                self.itogo.append([
                    index,
                    '',
                    self.experts.getList()[index].probability[len(self.experts.getList()[index].probability) - 1],
                    self.experts.getList()[index].answers.count(False) / float(len(self.experts.getList()[index].answers))
                ])
        table = AsciiTable(self.itogo)
        print table.table

    # Рачитываем потерю эксперта l
    def function_regret(self, result, resultTrue, expert):
        self.set_result_expert(result, resultTrue, expert)
        return math.pow(resultTrue - result, 2)

    # Добавляем ответ эксперта в массив
    def set_result_expert(self, result, resultTrue, expert):
        if (result == resultTrue):
            expert.answers.append(True)
        else:
            expert.answers.append(False)

    # Проход по экспертам
    def walk_experts(self, i, h, image):
        for expert in self.experts.getList():
            expert.predict(image)

    # Выбор результата менеджера
    def choise_true_result(self, i):
        rnd = numpy.random.random()
        item = self.experts.getList()[0]

        for expert in self.experts.getList():
            if (item.probability[i] < expert.probability[i] and expert.probability[i] > rnd):
                item = expert
        return item.lastResult

    # Установка вероятностей выбора картинки
    def set_probablity_images(self, imagesIndexs):
        data = self.nature.getData()
        countImages=len(imagesIndexs)
        numpy.random.seed(100)
        #probArr = 2.5 * numpy.random.randn((countImages-1)) + 3
        probArr=numpy.random.random_sample(((countImages-1),))
        probArr.sort()
        #prob= prob[::-1]
        j=0
        for i in imagesIndexs:
            if j==0:
                self.images.append([data[0][i], data[1][i], probArr[j], i, self.experts.getList()[i]])
            else:
                if j==(countImages-1):
                    self.images.append([data[0][i], data[1][i], 1-probArr[j-1], i, self.experts.getList()[i]])
                else:
                    self.images.append([data[0][i], data[1][i], probArr[j]-probArr[j-1], i, self.experts.getList()[i]])
            j=j+1
    # Получение картинки по заданой вероятности
    def get_image(self, i):
        rnd = numpy.random.random()
        prob=0.
        for image in self.images:
            prob=prob+image[2]
            if (prob > rnd):
               item=image
               return item[i]



    # Обновление весов экспертов
    def set_weight_experts(self, result):
        for expert in self.experts.getList():
            expert.weight.append(expert.weight[len(expert.weight)-1] * math.exp((-1) * self.h * self.function_regret(expert.lastResult, result, expert)))

    # Обновление вероятностей экспертов
    def set_probablity_experts(self):
        countWight = self.get_sum_weight_experts()
        for expert in self.experts.getList():
            expert.probability.append(expert.weight[-1]/float(countWight))

    # Получить сумму весов экспертов
    def get_sum_weight_experts(self):
        result = 0
        for expert in self.experts.getList():
            result = result + expert.weight[-1]
        return result

    # Печать графика
    def report(self):
        fig, ax = plt.subplots()
        plt.plot(self.faults)
        ax.set_xlabel(r'epochs')
        ax.set_ylabel(r'error')
        pylab.show()
