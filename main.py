import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.font as tkFont

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import DataHandler as dh
import os.path


# fit matplotlib charts normally
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})




class App:
    def __init__(self, root):
        # DataHandler instance
        self.DataHandler = dh.DataHandler()
        
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
                #LOAD FILE
                self.DataHandler.load_file(filePath)
                #DISPLAY CITIES IN COMBOBOX AND PUT FILE NAME ON LABEL
                self._gCombo_city['values'] = self.DataHandler.list_cities()
                self._gLabel_path["text"] = os.path.basename(filePath)
            except OSError as err:
                print(f"Cannot import file {filePath}.\nOS error: {err}\nExit.")
                # TODO:  show some gui error about file
            except:
                print("Some error happend during opening csv file")
                # TODO: show some gui error message
        else:
            print("No file selected. (or not ordinary file selected)")

   
    def hCombo_city_selected(self, event=None):
        selected_city = self._gCombo_city.get()
        print(f"Selected city: {selected_city}")
       
        #SELECT MONTHS FOR DATA TO BE DISPLAYED
        from_month = 4
        to_month = 12
        #NAME OF X-AXIS ACCORDING TO MONTH SELECTION
        x_axis = f'months [from {from_month} to {to_month}]'
        y_axis='energy [kwh]'
        
        #SET RANGE FOR DATA
        def range_plot(self, from_month, to_month):
            return range(from_month, to_month+1)
        
        #PLOT CHARTS
        def upleft(self):
            # UP LEFT FIGURE
            self.ax1.clear()
            self.ax1.bar(range_plot(self,from_month, to_month),
                         (self.DataHandler.kwh(from_month, to_month,selected_city).mean()))
            self.ax1.set_title('KWH average value per month')
            self.ax1.set_xlabel(x_axis); self.ax1.set_ylabel(y_axis)
            self.chart1.draw()

        def upright(self):
            # UP RIGHT FIGURE
            self.ax2.clear()
            self.ax2.bar(range_plot(self,from_month, to_month),
                         (self.DataHandler.therm(from_month,to_month,selected_city).mean()))
            self.ax2.set_title('THERM average value per month')
            self.ax2.set_xlabel(x_axis); self.ax2.set_ylabel(y_axis)
            self.chart2.draw()

        def botleft(self):
            # BOTTOM LEFT FIGURE
            self.ax3.clear()
            self.ax3.plot(range_plot(self,from_month, to_month),
                    (self.DataHandler.kwh(from_month, to_month,selected_city).max()),
                    color='red', marker ='*')
            self.ax3.plot(range_plot(self,from_month, to_month),
                    (self.DataHandler.kwh(from_month, to_month,selected_city).mean()),
                    color='blue', marker='s')
            self.ax3.set_title('KWH max and mean values per month')
            self.ax3.set_xlabel(x_axis); self.ax3.set_ylabel(y_axis)
            self.chart3.draw()

        def botfig(self):
            # BOTTOM RIGHT FIGURE
            self.ax4.clear()
            self.ax4.plot(range_plot(self,from_month, to_month),
                    (self.DataHandler.therm(from_month,to_month,selected_city).max()),
                    color='red', marker='*')
            self.ax4.plot(range_plot(self,from_month, to_month),
                    (self.DataHandler.therm(from_month,to_month,selected_city).mean()),
                    color='blue', marker='s')
            self.ax4.set_title('THERM max and mean values per month')
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
