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
        self.critical_value_of_correlation = 0.55


    def loadFile(self, fileName):
        with open(fileName) as plik:
            table = [list(map(float, wiersz.split(' '))) for wiersz in plik]
        print(table)
        return table

    def get_matrix(self):
        return self.matrix

    def analise_graph(self):
        for i in range(len(self.results.matrixR)):
            for j in range(len(self.results.matrixR[i])):
                if math.fabs(self.results.matrixR[i][j]) < self.critical_value_of_correlation:
                    self.results.matrixR[i][j] = 0
        print(self.results.matrixR)
        self.find_all_groups()
        for set in self.results.groups_in_graph:
            if len(set) > 1:
                self.find_bests_from_group(set)
        print(self.results.chosen_values_from_graphs)

    def already_in_group(self, number):
        for i in range(len(self.results.groups_in_graph)):
            if number in self.results.groups_in_graph[i]:
                return True
        return False

    def find_all_groups(self):
        for i in range(len(self.results.matrixR)):
            temporary_set = set()
            for j in range(len(self.results.matrixR[i])):
                if self.results.matrixR[i][j] != 0:
                    if not self.already_in_group(j):
                        temporary_set.add(j)
                        temporary_set.add(i)
            if len(temporary_set) > 0:
                self.results.groups_in_graph.append(temporary_set)
        print("sets ", self.results.groups_in_graph)

    def find_bests_from_group(self, set):
        most_connections = 0
        most_connected_values = []
        for value in set:
            count_connections = 0
            for j in range(len(self.results.matrixR[value])):
                if self.results.matrixR[value][j] != 0 and self.results.matrixR[value][j] <= 0.9999:
                    count_connections += 1
                    # print("went in ")
            if count_connections > most_connections:
                most_connections = count_connections
                most_connected_values = []
                most_connected_values.append(value)
            elif count_connections == most_connections:
                most_connected_values.append(value)
        highest_ratio = 0
        for connected in most_connected_values:
            if  math.fabs(self.results.matrixR0[connected]) > highest_ratio:
                highest_ratio = self.results.matrixR0[connected]
        for connected in most_connected_values:
            # print("compare ", round(self.results.matrixR0[connected], 3), "with", round(highest_ratio, 3))
            if math.fabs(round(self.results.matrixR0[connected], 3)) == round(highest_ratio, 3):
                # print("went in")
                self.results.chosen_values_from_graphs.append(connected)

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
        self.results.matrixR0 = np.corrcoef(self.matrix_after_calculations)
        self.results.matrixR0 = self.results.matrixR0[1:, 0]
        print("matrix r0", self.results.matrixR0)


    def count_matrixR(self):
        self.results.matrixR = np.corrcoef(self.matrix_after_calculations[1:])
        print("matrix r", self.results.matrixR)

    def get_x(self):
        return self.matrix_size_x

    def get_y(self):
        return self.matrix_size_y

    def preparation_for_display(self):
        self.count_average_in_all_columns()
        self.count_standard_deviation()
        self.count_coefficient_of_random_variable()
        self.discard_useless_data()
        self.get_matrix_after_calculations()
        self.count_matrixR0()
        self.count_matrixR()
        self.analise_graph()
        self.method_KMNK()

    def discard_useless_data(self):
        a = 0.1
        for i in range(len(self.results.coefficient_of_random_variable)):
            if (self.results.coefficient_of_random_variable[i] < a):
                self.blacklist.append(i)
        print(self.blacklist)

    def get_matrix_after_calculations(self):
        self.matrix_after_calculations = np.transpose(self.matrix)
        for i in range(len(self.blacklist)):
            self.matrix_after_calculations = np.delete(self.matrix_after_calculations, self.blacklist[i]-i+1, 0)
        print(self.matrix_after_calculations)

    def method_KMNK(self):
        pass