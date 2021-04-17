import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.font as tkFont

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import os.path
# fit matplotlib charts normally
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


class DataHandler:
    #init fun - what inside?
    def load_file(self, filePath):
        self.__df = pd.read_csv(filePath)
        self.__df = self.__df.dropna()
        
        
    def list_cities(self):
        vals = list(self.__df['COMMUNITY AREA NAME'].unique())
        vals.sort()
        return vals
    
    
    def data_city(self):#displays data for chosen city
        selected_city = self._gCombo_city.get()
        print(f"Selected city: {selected_city}")
        self.__subdf = self.__df.loc[self.__df['COMMUNITY AREA NAME']== selected_city].rename(columns={"TERM APRIL 2010":"THERM APRIL 2010"})
        return self.__subdf
    
    
    def kwh(self, from_month, to_month):#display kwh columns for selected city
        start = self.__subdf.columns.get_loc("KWH " + from_month + " 2010")
        end = self.__subdf.columns.get_loc("KWH " + to_month + " 2010")+1
        return self.__subdf.iloc[:,  range(start, end)]
    
    
    def therm(self, from_month, to_month):#display kwh columns for selected city
        start = self.__subdf.columns.get_loc("THERM " + from_month + " 2010")
        end = self.__subdf.columns.get_loc("THERM " + to_month + " 2010")+1
        return self.__subdf.iloc[:,  range(start, end)]
    
    def range_plot(self, from_month, to_month):
        start = self.__subdf.columns.get_loc("THERM " + from_month + " 2010")
        end = self.__subdf.columns.get_loc("THERM " + to_month + " 2010")+2
        return range(1, end-start)

class App:
    def __init__(self, root):
        # setting title
        root.title("Power histogram maker GUI")
        
        # get current dpi
        dpi = root.winfo_fpixels('1i')
        print(f"Current dpi is set to {dpi}")

        # frame for buttons and other controls..
        self._gF_controls = tk.Frame(root)
        self._gF_controls.pack(ipadx=10, ipady=10)

        # frame for charts
        self._gF_graphs = tk.Frame(root)
        self._gF_graphs.pack(side=tk.BOTTOM,
                             padx=5, pady=5,
                             fill=tk.BOTH, expand=True)

        self._gButton_open = tk.Button(self._gF_controls)
        self._gButton_open["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=12)
        self._gButton_open["font"] = ft
        self._gButton_open["fg"] = "#000000"
        self._gButton_open["justify"] = "center"
        self._gButton_open["text"] = "Open csv..."
        self._gButton_open.pack(side=tk.LEFT,
                                ipadx=10)
        self._gButton_open["command"] = self.hButton_open_command

        # LABEL FOR CSV FILE SELECTED
        self._gLabel_path = tk.Label(self._gF_controls)
        ft = tkFont.Font(family='Times', size=10)
        self._gLabel_path["font"] = ft
        self._gLabel_path["fg"] = "#333333"
        self._gLabel_path["justify"] = "center"
        self._gLabel_path["text"] = "no file selected"
        self._gLabel_path.pack(side=tk.LEFT,
                               ipadx=10)

        # COMBOBOX
        self._gCombo_city = ttk.Combobox(self._gF_controls, state='readonly')
        self._gCombo_city.pack(side=tk.RIGHT)
        self._gCombo_city.bind("<<ComboboxSelected>>",
                               self.hCombo_city_selected)

        self._gLabel_combo = tk.Label(self._gF_controls)
        ft = tkFont.Font(family='Times', size=12)
        self._gLabel_combo["font"] = ft
        self._gLabel_combo["fg"] = "#333333"
        self._gLabel_combo["justify"] = "center"
        self._gLabel_combo['text'] = "Select city"
        self._gLabel_combo.pack(side=tk.LEFT)

        # TODO: fake chart with text "no data to graph"

        self._gCanvas_upleft = tk.Frame(self._gF_graphs)
        self._gCanvas_upleft.place(relx=0, rely=0,
                                   relwidth=0.5, relheight=0.5)
        fig = plt.figure(dpi=dpi)
        self.ax1 = fig.add_subplot(111)
        self.ax1.text(0.1,0.5,"choose file then city to display data", fontsize=10)
        self.chart1 = FigureCanvasTkAgg(fig, self._gCanvas_upleft)
        self.chart1.get_tk_widget().pack(padx=5, pady=5,
                                         side=tk.BOTTOM,
                                         fill=tk.BOTH, expand=True)

        self._gCanvas_upright = tk.Frame(self._gF_graphs)
        self._gCanvas_upright.place(relx=0.5, rely=0,
                                    relwidth=0.5, relheight=0.5)
        fig = plt.figure(dpi=dpi)
        self.ax2 = fig.add_subplot(111)
        self.ax2.text(0.1,0.5,"choose file then city to display data", fontsize=10)
        self.chart2 = FigureCanvasTkAgg(fig, self._gCanvas_upright)
        self.chart2.get_tk_widget().pack(padx=5, pady=5,
                                         side=tk.BOTTOM,
                                         fill=tk.BOTH, expand=True)

        self._gCanvas_botleft = tk.Frame(self._gF_graphs)
        self._gCanvas_botleft.place(relx=0, rely=0.5,
                                    relwidth=0.5, relheight=0.5)
        fig = plt.figure(dpi=dpi)
        self.ax3 = fig.add_subplot(111)
        self.ax3.text(0.1,0.5,"choose file then city to display data", fontsize=10)
        self.chart3 = FigureCanvasTkAgg(fig, self._gCanvas_botleft)
        self.chart3.get_tk_widget().pack(padx=5, pady=5,
                                         side=tk.BOTTOM,
                                         fill=tk.BOTH, expand=True)

        self._gCanvas_botright = tk.Frame(self._gF_graphs)
        self._gCanvas_botright.place(relx=0.5, rely=0.5,
                                     relwidth=0.5, relheight=0.5)
        fig = plt.figure(dpi=dpi)
        self.ax4 = fig.add_subplot(111)
        self.ax4.text(0.1,0.5,"choose file then city to display data", fontsize=10)
        self.chart4 = FigureCanvasTkAgg(fig, self._gCanvas_botright)
        self.chart4.get_tk_widget().pack(padx=5, pady=5,
                                         side=tk.BOTTOM,
                                         fill=tk.BOTH, expand=True)
        
        

    def hButton_open_command(self):
        filetypes = (
            ('CSV files', '*.csv'),
            ('All files', '*.*'))

        filePath = fd.askopenfilename(
                title='Open a CSV file ...',
                initialdir='./',
                filetypes=filetypes)
        
        if os.path.isfile(filePath):
            try:
                DataHandler.load_file(self, filePath)
                                
                self._gCombo_city['values'] = DataHandler.list_cities(self)
                self._gLabel_path["text"] = os.path.basename(filePath)
            except OSError as err:
                print(f"Cannot import file {filePath}.\nOS error: {err}\nExit.")
                # TODO:  show some gui error about file
            except:
                print("Some error happend during opening csv file")
                # TODO: show some gui error message
        else:
            print("No file selected. (or not ordinary file selected)")

    # desired behavior: select one area,
    # show 4 plots drawn on 4 canvases of that area:
    # top left: bar chart, average KWH by month
    # top right: bar chart, average THERM by month
    # bottom left and bottom right up to you
    def hCombo_city_selected(self, event=None):

        
        DataHandler.data_city(self)
        
        from_month = "FEBRUARY"
        to_month = "JULY"
        #name of x-axis according to months selection
        x_axis = f'months [from {from_month} to {to_month}]'
        y_axis='energy [kwh]'

        def upleft(self):
            # UP LEFT FIGURE
            self.ax1.clear()
            self.ax1.bar(DataHandler.range_plot(self, from_month, to_month),#set range for selected months
                         (DataHandler.kwh(self, from_month, to_month).mean()))
            self.ax1.set_title('KWH average value per month')
            self.ax1.set_xlabel(x_axis); self.ax1.set_ylabel(y_axis)
            self.chart1.draw()

        def upright(self):
            # UP RIGHT FIGURE
            self.ax2.clear()
            self.ax2.bar(DataHandler.range_plot(self, from_month, to_month),
                         (DataHandler.therm(self,from_month,to_month).mean()))
            self.ax2.set_title('THERM average value per month')
            self.ax2.set_xlabel(x_axis); self.ax2.set_ylabel(y_axis)
            self.chart2.draw()

        def botleft(self):
            # BOTTOM LEFT FIGURE
            self.ax3.clear()
            self.ax3.plot(DataHandler.range_plot(self, from_month, to_month),
                    (DataHandler.kwh(self, from_month, to_month).max()),
                    color='red', marker ='*')
            self.ax3.plot(DataHandler.range_plot(self, from_month, to_month),
                    (DataHandler.kwh(self, from_month, to_month).mean()),
                    color='blue', marker='s')
            self.ax3.set_title('KWH maximum and min values per month')
            self.ax3.set_xlabel(x_axis); self.ax3.set_ylabel(y_axis)
            self.chart3.draw()

        def botfig(self):
            # BOTTOM RIGHT FIGURE
            self.ax4.clear()
            self.ax4.plot(DataHandler.range_plot(self, from_month, to_month),
                    (DataHandler.therm(self,from_month,to_month).max()),
                    color='red', marker='*')
            self.ax4.plot(DataHandler.range_plot(self, from_month, to_month),
                    (DataHandler.therm(self,from_month,to_month).mean()),
                    color='blue', marker='s')
            self.ax4.set_title('THERM max and min values per month')
            self.ax4.set_xlabel(x_axis); self.ax4.set_ylabel(y_axis)
            self.chart4.draw()

        upleft(self)
        upright(self)
        botleft(self)
        botfig(self)


def main():
    root = tk.Tk()
    app = App(root)
    root.geometry("800x600")

    # setting in True  enable to resize window when displayed
    root.resizable(width=True, height=True)

    # root.geometry() will return '1x1+www+hhh' here
    root.update()

    # now root.geometry() returns valid size/placement
    root.minsize(root.winfo_width(), root.winfo_height())

    root.mainloop()


if __name__ == "__main__":
    main()
