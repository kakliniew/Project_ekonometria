import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
from matrixOperations import *


class GraphicalInterface:
    def __init__(self, fileName):
        self.root = tk.Tk()
        self.mymatrix = MatrixOperations(fileName)
        self.mymatrix.update_size()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nswe")
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky="nswe")
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky="nswe")

    def create_interface(self):
        self.mymatrix.preparation_for_display()
        self.add_data_view()
        self.add_result_view()
        self.add_field_with_calculations()
        self.add_graphs()

        # self.add_chart()



    def start_application(self):
        self.create_interface()
        self.root.mainloop()

    def add_chart(self):
        data1 = {'Country': ['US', 'CA', 'GER', 'UK', 'FR'],
                 'GDP_Per_Capita': [45000, 42000, 52000, 49000, 47000]
                 }
        df1 = DataFrame(data1, columns=['Country', 'GDP_Per_Capita'])
        figure1 = plt.Figure(figsize=(6, 5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self.left_frame)
        bar1.get_tk_widget().grid(row=50, column =50)
        df1 = df1[['Country', 'GDP_Per_Capita']].groupby('Country').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Country Vs. GDP Per Capita')

    def add_data_view(self):
        for i in range(len(self.mymatrix.matrix[0])):
            e = tk.Entry(self.left_frame, width=10, fg='blue',
                         font=('Arial', 16, 'bold'))
            e.grid(row=0, column=i)
            if i == 0 :
                e.insert(tk.END, "y")
            else:
                e.insert(tk.END, "x" + str(i-1))
        for i in range(len(self.mymatrix.matrix)):
            for j in range(len(self.mymatrix.matrix[0])):
                if j-1 not in self.mymatrix.blacklist:
                    e = tk.Entry(self.left_frame, width=10, fg='blue',
                                   font=('Arial', 16, 'bold'))
                    e.grid(row=i+1, column=j)
                    e.insert(tk.END, self.mymatrix.get_matrix()[i][j])
                else:
                    e = tk.Entry(self.left_frame, width=10, fg='red',
                                 font=('Arial', 16, 'bold'))
                    e.grid(row=i+1, column=j)
                    e.insert(tk.END, self.mymatrix.get_matrix()[i][j])


    def add_result_view(self):
        e = tk.Entry(self.left_frame, width=10, fg='green',
                     font=('Arial', 16, 'bold'))
        e.grid(row=len(self.mymatrix.matrix) + 1, column=0)
        e.insert(tk.END, "Average")
        for i in range(len(self.mymatrix.results.average)):
           e = tk.Entry(self.left_frame, width=10, fg='green',
                        font=('Arial', 16, 'bold'))
           e.grid(row=len(self.mymatrix.matrix)+1, column=i+1)
           e.insert(tk.END, round(self.mymatrix.results.average[i], 4))

        e = tk.Entry(self.left_frame, width=10, fg='green',
                     font=('Arial', 16, 'bold'))
        e.grid(row=len(self.mymatrix.matrix) + 2, column=0)
        e.insert(tk.END, "Deviation")
        for i in range(len(self.mymatrix.results.deviation)):
            e = tk.Entry(self.left_frame, width=10, fg='green',
                         font=('Arial', 16, 'bold'))
            e.grid(row=len(self.mymatrix.matrix) + 2, column=i + 1)
            e.insert(tk.END, round(self.mymatrix.results.deviation[i], 4))

        e = tk.Entry(self.left_frame, width=10, fg='green',
                     font=('Arial', 16, 'bold'))
        e.grid(row=len(self.mymatrix.matrix) + 3, column=0)
        e.insert(tk.END, "Coeff of random var")
        for i in range(len(self.mymatrix.results.coefficient_of_random_variable)):
            if self.mymatrix.results.coefficient_of_random_variable[i] > 0.1:
                e = tk.Entry(self.left_frame, width=10, fg='green',
                             font=('Arial', 16, 'bold'))
            else:
                e = tk.Entry(self.left_frame, width=10, fg='red',
                             font=('Arial', 16, 'bold'))
            e.grid(row=len(self.mymatrix.matrix) + 3, column=i + 1)
            e.insert(tk.END, round(self.mymatrix.results.coefficient_of_random_variable[i], 4))


    def add_graphs(self):
        pass

    def add_field_with_calculations(self):
        e = tk.Text(self.right_frame, height=20, width=110)
        e.grid(row=0, column=self.mymatrix.get_x())
        e.grid_rowconfigure(0, weight=15)
        e.grid_columnconfigure(0, weight=15)
        e.insert(tk.END, self.mymatrix.calculations_string)
