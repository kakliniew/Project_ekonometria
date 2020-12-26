import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matrixOperations import *
from matplotlib.figure import Figure
import networkx as nx

class GraphicalInterface:
    def __init__(self, fileName):
        self.root = tk.Tk()
        self.mymatrix = MatrixOperations(fileName)
        self.mymatrix.update_size()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nswe")
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky="nswe")
        self.left_frame_first = tk.Frame(self.left_frame)
        self.left_frame_first.grid(row=0, column=0, sticky="nswe")
        self.left_frame_second = tk.Frame(self.left_frame)
        self.left_frame_second.grid(row=1, column=0, sticky="nswe")
        self.left_frame_third = tk.Frame(self.left_frame)
        self.left_frame_third.grid(row=2, column=0, sticky="nswe")
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky="nswe")
        self.right_frame_first = tk.Frame(self.right_frame)
        self.right_frame_first.grid(row=0, column=0, sticky="nswe")
        self.right_frame_second = tk.Frame(self.right_frame)
        self.right_frame_second.grid(row=1, column=0, sticky="nswe")
        self.right_frame_third = tk.Frame(self.right_frame)
        self.right_frame_third.grid(row=2, column=0, sticky="nswe")
        self.G = nx.Graph()


    def create_interface(self):
        self.mymatrix.preparation_for_display()
        self.add_data_view()
        self.add_result_view()
        self.add_field_with_calculations()
        if len(self.mymatrix.results.chosen_values_from_graphs) > 0:
            self.add_graphs()
            self.add_model_equation()
            self.add_chart()




    def start_application(self):
        self.create_interface()
        self.root.mainloop()

    def add_chart(self):
        x = []
        for value in self.mymatrix.results.chosen_values_from_graphs:
            values_of_x = self.mymatrix.matrix_after_calculations[value+1]
            print(values_of_x)
            x.append(values_of_x)
        y2 = self.mymatrix.matrix_after_calculations[0]
        y = 0
        for i in range(len(x)):
            y += np.asarray(x[i]) * self.mymatrix.results.value_a[i]
        y += self.mymatrix.results.value_a[len(self.mymatrix.results.value_a)-1]

        fig = Figure(figsize=(6, 6))
        a = fig.add_subplot(111)
        a.plot(y, color='blue', label="model")
        a.plot(y2, color='red', label="pomiar")
        a.legend(loc="upper left")
        a.set_title("Porownanie modelu z pomiarem", fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("X", fontsize=14)
        canvas2 = FigureCanvasTkAgg(fig, master=self.left_frame_second)
        canvas2.get_tk_widget().grid(row=0, column=0)
        canvas2.draw()

    def add_data_view(self):
        for i in range(len(self.mymatrix.matrix[0])):
            e = tk.Text(self.left_frame_first, width=10, height = 1, fg='blue',
                         font=('Arial', 16, 'bold'))
            e.grid(row=0, column=i)
            if i == 0 :
                e.insert(tk.END, "y")
            else:
                e.insert(tk.END, "x" + str(i-1))
        for i in range(len(self.mymatrix.matrix)):
            for j in range(len(self.mymatrix.matrix[0])):
                if j-1 not in self.mymatrix.blacklist:
                    e = tk.Text(self.left_frame_first, width=10, height = 1, fg='blue',
                                   font=('Arial', 16, 'bold'))
                    e.grid(row=i+1, column=j)
                    e.insert(tk.END, self.mymatrix.get_matrix()[i][j])
                else:
                    e = tk.Text(self.left_frame_first, width=10, height = 1, fg='red',
                                 font=('Arial', 16, 'bold'))
                    e.grid(row=i+1, column=j)
                    e.insert(tk.END, self.mymatrix.get_matrix()[i][j])


    def add_result_view(self):
        e = tk.Text(self.left_frame_first, width=10, height = 1, fg='green',
                     font=('Arial', 16, 'bold'))
        e.grid(row=len(self.mymatrix.matrix) + 1, column=0)
        e.insert(tk.END, "Average")
        for i in range(len(self.mymatrix.results.average)):
           e = tk.Text(self.left_frame_first, width=10, height = 1, fg='green',
                        font=('Arial', 16, 'bold'))
           e.grid(row=len(self.mymatrix.matrix)+1, column=i+1)
           e.insert(tk.END, round(self.mymatrix.results.average[i], 4))

        e = tk.Text(self.left_frame_first, width=10, height = 1, fg='green',
                     font=('Arial', 16, 'bold'))
        e.grid(row=len(self.mymatrix.matrix) + 2, column=0)
        e.insert(tk.END, "Deviation")
        for i in range(len(self.mymatrix.results.deviation)):
            e = tk.Text(self.left_frame_first, width=10, height = 1, fg='green',
                         font=('Arial', 16, 'bold'))
            e.grid(row=len(self.mymatrix.matrix) + 2, column=i + 1)
            e.insert(tk.END, round(self.mymatrix.results.deviation[i], 4))

        e = tk.Text(self.left_frame_first, width=10, height = 1, fg='green',
                     font=('Arial', 16, 'bold'))
        e.grid(row=len(self.mymatrix.matrix) + 3, column=0)
        e.insert(tk.END, "Coeff of random var")
        for i in range(len(self.mymatrix.results.coefficient_of_random_variable)):
            if self.mymatrix.results.coefficient_of_random_variable[i] > 0.1:
                e = tk.Text(self.left_frame_first, width=10, height = 1, fg='green',
                             font=('Arial', 16, 'bold'))
            else:
                e = tk.Text(self.left_frame_first, width=10, height = 1, fg='red',
                             font=('Arial', 16, 'bold'))
            e.grid(row=len(self.mymatrix.matrix) + 3, column=i + 1)
            e.insert(tk.END, round(self.mymatrix.results.coefficient_of_random_variable[i], 4))


    def add_graphs(self):
        for group in self.mymatrix.results.groups_in_graph:
            for value in group:
                for j in range(len(self.mymatrix.results.matrixR[value])):
                    if self.mymatrix.results.matrixR[value][j] != 0:
                        self.G.add_edge(value, j)
        f = plt.figure(figsize=(5, 4))
        plt.axis('off')
        pos = nx.circular_layout(self.G)
        nx.draw_networkx(self.G, pos=pos, node_color='r', edge_color='b')
        canvas = FigureCanvasTkAgg(f, master=self.right_frame_second)
        canvas.get_tk_widget().grid(row=0, column=0)


    def add_field_with_calculations(self):
        e = tk.Text(self.right_frame_first, height=20, width=110)
        e.grid(row=0, column=self.mymatrix.get_x())
        e.grid_rowconfigure(0, weight=15)
        e.grid_columnconfigure(0, weight=15)
        e.insert(tk.END, self.mymatrix.calculations_string)

    def add_model_equation(self):
        model_equation = "yi = "
        print(self.mymatrix.results.value_D)
        for i in range(len(self.mymatrix.results.value_a)-1):
            model_equation += str(round(self.mymatrix.results.value_a[i], 4)) + " x" + str(i) + " + "
        model_equation += str(round(self.mymatrix.results.value_a[len(self.mymatrix.results.value_D)-1], 4))
        e = tk.Text(self.right_frame_third, width=50, height=1, fg='black',
                    font=('Arial', 20, 'bold'))
        e.grid(row=0, column=0)
        e.insert(tk.END, model_equation)

        model_error = "      "
        for i in range(len(self.mymatrix.results.value_D)):
            model_error += "(" + str(round(self.mymatrix.results.value_D[i][i], 4)) + " )" + "   "
        e = tk.Text(self.right_frame_third, width=50, height=1, fg='black',
                    font=('Arial', 20, 'bold'))
        e.grid(row=1, column=0)
        e.insert(tk.END, model_error)