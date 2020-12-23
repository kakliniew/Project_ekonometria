from typing import List
import math
from results import *
import numpy as np

class MatrixOperations:
    matrix: List[List[float]]

    def __init__(self, fileName):
        self.matrix_size_x = 0
        self.matrix_size_y = 0
        self.matrix = MatrixOperations.loadFile(self, fileName)
        self.results = Results()
        self.blacklist = []
        self.matrix_after_calculations = [[]]


    def loadFile(self, fileName):
        with open(fileName) as plik:
            table = [list(map(float, wiersz.split(' '))) for wiersz in plik]
        print(table)
        return table

    def get_matrix(self):
        return self.matrix

    def aggregate_data(self):
        pass

    def analise_graph(self):
        pass

    def count_average_in_all_columns(self):
        for i in range(1,self.matrix_size_x):
            sum = 0
            for j in range(self.matrix_size_y):
                sum += self.matrix[j][i]
            self.results.average.append(sum/self.matrix_size_y)
        print("average ", self.results.average)

    def update_size(self):
        self.matrix_size_x = len(self.matrix[0])
        self.matrix_size_y = len(self.matrix)

    def count_standard_deviation(self):
        for i in range(1, self.matrix_size_x):
            sum = 0
            for j in range(self.matrix_size_y):
                sum += (self.matrix[j][i] - self.results.average[i-1])*(self.matrix[j][i] - self.results.average[i-1])
            self.results.deviation.append(math.sqrt(sum/(self.matrix_size_y-1)))
        print("deviations ", self.results.deviation)

    def count_coefficient_of_random_variable(self):
        for i in range(1, self.matrix_size_x):
            self.results.coefficient_of_random_variable.append(self.results.deviation[i-1]/self.results.average[i-1])
        print("coefficient of random ", self.results.coefficient_of_random_variable)

    def count_matrixR0(self):
        self.results.matrixR0 = np.corrcoef(np.transpose(self.matrix_after_calculations))
        print("matrix r0", self.results.matrixR0)


    def count_matrixR(self):
        self.results.matrixR = np.corrcoef(self.matrix_after_calculations[1:])
        print("matrix r", self.results.matrixR)

    def get_x(self):
        return self.matrix_size_x

    def get_y(self):
        return self.matrix_size_y

    def preparation_for_display(self):
        self.aggregate_data()
        self.count_average_in_all_columns()
        self.count_standard_deviation()
        self.count_coefficient_of_random_variable()
        self.discard_useless_data()
        self.get_matrix_after_calculations()
        self.count_matrixR0()
        self.count_matrixR()
        self.analise_graph()

    def discard_useless_data(self):
        a = 0.1
        for i in range(len(self.results.coefficient_of_random_variable)):
            if (self.results.coefficient_of_random_variable[i] < a):
                self.blacklist.append(i)
        print(self.blacklist)

    def get_matrix_after_calculations(self):
        self.matrix_after_calculations = np.transpose(self.matrix)
        # self.matrix_after_calculations = self.matrix_after_calculations[1:]
        # print(self.matrix_after_calculations)
        # self.matrix_after_calculations
        for i in range(len(self.blacklist)):
            self.matrix_after_calculations = np.delete(self.matrix_after_calculations, self.blacklist[i]-i+1, 0)
        # print(self.matrix_after_calculations)