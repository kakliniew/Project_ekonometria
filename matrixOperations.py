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
        self.calculations_string = ""


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
        self.calculations_string += "Obliczono macierz R i R0 i wyzerowano w macierzy R wartości, których wartość bezwzględna < " + str(self.critical_value_of_correlation) + " \n"
        self.find_all_groups()
        for set in self.results.groups_in_graph:
            if len(set) > 1:
                self.find_bests_from_group(set)
            else:
                self.calculations_string += "Z grupy " + str(set)
                for value in set:
                    if self.results.matrixR0[value] > self.critical_value_of_correlation:
                        self.calculations_string += " wybrano wartość " + str(value) + "\n"
                        self.results.chosen_values_from_graphs.append(value)
                    else:
                        self.calculations_string += " nie wybrano wartosci, poniewaz wspolczynnik w R0 jest mniejszy niz wartosc krytyczna "+ str(self.critical_value_of_correlation) + "\n"



        print(self.results.chosen_values_from_graphs)

    def already_in_group(self, number):
        for i in range(len(self.results.groups_in_graph)):
            if number in self.results.groups_in_graph[i]:
                return True
        return False

    def append_index_to_existing_set(self, existing_value, appending_value):
        for set in self.results.groups_in_graph:
            if existing_value in set:
                set.add(appending_value)

    def find_all_groups(self):
        for i in range(len(self.results.matrixR)):
            temporary_set = set()
            for j in range(len(self.results.matrixR[i])):
                if self.results.matrixR[i][j] != 0:
                    if not self.already_in_group(j):
                        if not self.already_in_group(i):
                            temporary_set.add(j)
                            temporary_set.add(i)
                        else:
                            self.append_index_to_existing_set(i, j)
            if len(temporary_set) > 0:
                self.results.groups_in_graph.append(temporary_set)
        self.calculations_string += "Na podstawie tabeli R ustalono grupy: " + str(self.results.groups_in_graph) + "\n"
        print("sets ", self.results.groups_in_graph)

    def find_bests_from_group(self, set):
        most_connections = 0
        most_connected_values = []
        self.calculations_string += "Z grupy " + str(set) + " wybrano wartości: "
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
        print("najwiecej polaczonych z setu ma ", most_connected_values)
        self.calculations_string += str(most_connected_values) + ", ponieważ mają najwiecej polaczen \n"
        for connected in most_connected_values:
            if  math.fabs(self.results.matrixR0[connected]) > highest_ratio:
                highest_ratio = self.results.matrixR0[connected]
        self.calculations_string += "Spośrod nich wybrano podane wartości z najwyzszym wspólczynnikiem w R0 = " + str(round(highest_ratio,3)) + " , a są to: "
        for connected in most_connected_values:
            print("compare ", round(self.results.matrixR0[connected], 3), "with", round(highest_ratio, 3))
            if math.fabs(round(self.results.matrixR0[connected], 3)) == math.fabs(round(highest_ratio, 3)):
                print("went in")
                self.calculations_string += str(connected) + ", "
                self.results.chosen_values_from_graphs.append(connected)
        self.calculations_string += "\n"


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
        if len(self.results.chosen_values_from_graphs) > 0 :
            self.method_KMNK()
            self.model_verification()
        else:
            self.calculations_string += "Nie wybrano z grafów żadnej wartości, dlatego, nie jest możliwe dalsze ustalanie modelu \n"

    def discard_useless_data(self):
        a = 0.1
        self.calculations_string += "Ze względu na małą korelację( < " + str(a) + ") nie będa brane pod uwage zmienne: "
        for i in range(len(self.results.coefficient_of_random_variable)):
            if (self.results.coefficient_of_random_variable[i] < a):
                self.calculations_string += "X" + str(i) + " "
                self.blacklist.append(i)
        print(self.blacklist)
        self.calculations_string += "\n"

    def get_matrix_after_calculations(self):
        self.matrix_after_calculations = np.transpose(self.matrix)
        for i in range(len(self.blacklist)):
            self.matrix_after_calculations = np.delete(self.matrix_after_calculations, self.blacklist[i]-i+1, 0)
        print("matrix after calculations", self.matrix_after_calculations)

    def method_KMNK(self):
        self.calculations_string += "Następnie zastosowano metodę KMNK: \n"
        for value in self.results.chosen_values_from_graphs:
            self.results.KMNK_X.append(self.matrix_after_calculations[value+1])
        self.results.KMNK_X.append(np.ones(len(self.results.KMNK_X[0])))
        self.calculations_string += "Wyznaczono nową macierz X oraz y \n"
        print("new macierz X", self.results.KMNK_X)
        self.results.KMNK_X = np.transpose(self.results.KMNK_X)
        x_t_x = np.matmul(np.transpose(self.results.KMNK_X), self.results.KMNK_X)
        x_t_y = np.matmul(np.transpose(self.results.KMNK_X), self.matrix_after_calculations[0])
        self.calculations_string += "Obliczono xTx oraz xTy \n"
        print(x_t_y)
        print(np.linalg.inv(x_t_x))
        self.results.value_a = np.matmul(np.linalg.inv(x_t_x), x_t_y)
        print(self.results.value_a)
        print(len(self.results.KMNK_X))
        print(len(self.results.KMNK_X[0]))
        y_t_y = np.matmul(np.transpose(self.matrix_after_calculations[0]), self.matrix_after_calculations[0])
        y_t_X_a = np.matmul(np.matmul(np.transpose(self.matrix_after_calculations[0]), self.results.KMNK_X), self.results.value_a)
        self.results.value_s2 = (1 / (len(self.results.KMNK_X) - len(self.results.KMNK_X[0])))*(y_t_y -y_t_X_a)
        self.calculations_string += "Obliczono s2 i otrzymano wartość: " + str(self.results.value_s2) + "\n"
        print(self.results.value_s2)
        temporary_value_D2 = np.absolute(self.results.value_s2 * np.linalg.inv(x_t_x))
        print("temporrary_value_d2 ", temporary_value_D2)
        self.results.value_D = np.sqrt(temporary_value_D2)
        self.calculations_string += "Następnie obliczono D2 i otrzymano model: \n"
        self.calculations_string += "yi = "
        for i in range(len(self.results.value_D)-1):
            self.calculations_string += str(round(self.results.value_D[i][i],4)) + " x" + str(i) + " + "
        self.calculations_string += str(round(self.results.value_D[len(self.results.value_D)-1][len(self.results.value_D)-1],5)) + " \n"
        print("D value ", self.results.value_D)

    def model_verification(self):
        for value in self.matrix_after_calculations[0]:
            self.results.sum_y += value
            self.results.sum_y_qtr +=  value ** 2
        self.results.value_fi_q = ((len(self.results.KMNK_X) - len(self.results.KMNK_X[0])) * self.results.value_s2) / (self.results.sum_y_qtr - (self.results.sum_y ** 2 / len(self.results.KMNK_X)))
        print("value fi^2 ", self.results.value_fi_q)
        self.calculations_string += "Następnie obliczono wartość fi^2 = " + str(self.results.value_fi_q) + "\n"
        self.calculations_string += "Wartość R^2 = " + str(1- self.results.value_fi_q) + "\n"
        self.results.value_vs = np.sqrt(self.results.value_s2) / (self.results.sum_y / len(self.results.KMNK_X)) * 100
        self.calculations_string += "oraz wartość vs = " + str(self.results.value_vs)  + " % \n"
        print(np.sqrt(self.results.value_s2))
        self.calculations_string += "Wartość Su = " + str(np.sqrt(self.results.value_s2)) + " \n"
        print("average Y ", (self.results.sum_y / len(self.results.KMNK_X)))
        print("value vs ", self.results.value_vs)
