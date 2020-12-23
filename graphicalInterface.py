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
        self.e = None

    def create_interface(self):
        self.mymatrix.preparation_for_display()
        self.add_data_view()
        self.add_field_with_calculations()
        self.add_graphs()
        self.add_chart()



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
        bar1 = FigureCanvasTkAgg(figure1, self.root)
        bar1.get_tk_widget().grid(row=15, column =15)
        df1 = df1[['Country', 'GDP_Per_Capita']].groupby('Country').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Country Vs. GDP Per Capita')

    def add_data_view(self):
        for i in range(len(self.mymatrix.matrix)):
            for j in range(len(self.mymatrix.matrix[0])):
                self.e = tk.Entry(self.root, width=10, fg='blue',
                               font=('Arial', 16, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, self.mymatrix.get_matrix()[i][j])

    def add_result_view(self):
        for i in range(len(self.mymatrix.resultMatrix)):
            for j in range(len(self.mymatrix.resultMatrix[0])):
                self.e = tk.Entry(self.root, width=10, fg='blue',
                                  font=('Arial', 16, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, self.mymatrix.get_matrix()[i][j])



    def add_graphs(self):
        pass

    def add_field_with_calculations(self):
        pass
