# referenced:
# https://www.youtube.com/watch?v=Zw6M-BnAPP0
# https://matplotlib.org/py-modindex.html
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://docs.python.org/3.5/





import tkinter as tk
from tkinter import ttk

import DataStructures
import DataParser

import datetime

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



class App(tk.Tk):

    def __init__(self, domains):

        tk.Tk.__init__(self)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Visualizations")


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        startPage = StartPage(container, self, domains)
        startPage.grid(row=0, column=0,sticky="nsew")
        self.frames[StartPage] = startPage

        domianPage = DomainPage(container, self)
        domianPage.grid(row=0, column=0,sticky="nsew")
        self.frames[DomainPage] = domianPage


        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_domain(self, domain):
        frame = self.frames[DomainPage]
        frame.set_Domain(domain)
        frame.tkraise()




class StartPage(tk.Frame):

    def __init__(self, parent, controller, domains):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page")
        label.pack(pady=10, padx=10)

        self.buttons = []
        for domain in domains:
            button = tk.Button(self, text=domain.name, command=lambda domain=domain: controller.show_domain(domain))
            button.pack(side=tk.TOP)
            self.buttons.append(button)


class DomainPage(tk.Frame):

    # self.colourButtonSelected =

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Page Two")
        self.label.pack(pady=10, padx=10, )

        button1 = ttk.Button(self, text="Go Home", command = lambda: controller.show_frame(StartPage))
        button1.pack()


        settingFrame = tk.Frame(self)
        settingFrame.pack()

        self.settingButtons = {}

        buttonComparePopularity = tk.Button(settingFrame, text="Popularity", command= lambda : self.compare_Popurarity())
        buttonComparePopularity.pack(side=tk.LEFT)
        self.settingButtons['buttonComparePopularity'] = buttonComparePopularity

        buttonCompareRelease_Frequency = tk.Button(settingFrame, text="Release Frequency", command= lambda : self.compare_Release_Frequency())
        buttonCompareRelease_Frequency.pack(side=tk.LEFT)
        self.settingButtons['buttonCompareRelease_Frequency'] = buttonCompareRelease_Frequency

        buttonCompareLast_Modification_Date = tk.Button(settingFrame, text="Set3")
        buttonCompareLast_Modification_Date.pack(side=tk.LEFT)
        self.settingButtons['buttonCompareLast_Modification_Date'] = buttonCompareLast_Modification_Date

        buttonComparePerformance = tk.Button(settingFrame, text="Set4")
        buttonComparePerformance.pack(side=tk.LEFT)
        self.settingButtons['buttonComparePerformance'] = buttonComparePerformance

        buttonCompareSecurity = tk.Button(settingFrame, text="Set5")
        buttonCompareSecurity.pack(side=tk.LEFT)
        self.settingButtons['buttonCompareSecurity'] = buttonCompareSecurity


        self.f = Figure(figsize=(5, 5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.f.subplots_adjust(bottom=0.5)

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # self.canvas.draw()



    def set_Domain(self, domain):
        self.domain = domain

        self.label.config(text=domain.name)

        self.compare_Popurarity()


    def compare_Popurarity(self):
        self.select_button('buttonComparePopularity')

        x = []
        heights = []
        names = []
        for i in range(len(self.domain.libraries)):
            x.append(i)
            heights.append(int(self.domain.libraries[i].popularity))
            names.append(self.domain.libraries[i].name)


        self.a.clear()
        # self.a.plot(x, heights)
        print(x)
        print(heights)
        print(names)

        self.a.bar(x, heights, tick_label=names)
        self.a.tick_params(axis='x', labelrotation = 45)

        # self.canvas.
        # self.canvas = FigureCanvasTkAgg(self.f, self)

        self.canvas.draw()


        print(self.a.get_xticks())

    def compare_Release_Frequency(self):
        self.select_button('buttonCompareRelease_Frequency')


        minDate = self.domain.libraries[0].releaseDates[0]
        maxDate = minDate

        # print(minDate)
        # print(minDate.year)

        plotLines = []

        self.a.clear()

        for library in self.domain.libraries:
            years = []
            counts = []
            for date in library.releaseDates:
                year = datetime.date(date.year, 1, 1)
                if year in years:
                    index = years.index(year)
                    counts[index] += 1
                else:
                    years.append(year)
                    counts.append(1)

            self.a.plot_date(matplotlib.dates.date2num(years), counts, ls='solid', label=library.name)

        self.a.legend()


        # self.a.plot_date(matplotlib.dates.date2num(self.domain.libraries[0].releaseDates), y1)
        # self.a.plot_date(matplotlib.dates.date2num(self.domain.libraries[1].releaseDates), y2)

        self.canvas.draw()



    def select_button(self, buttonName):
        """Sets only the given buttonName as disabled,(ie selected), and enables all the others"""
        for button in self.settingButtons.values():
            button.config(state=tk.ACTIVE)
        self.settingButtons[buttonName].config(state=tk.DISABLED)


domains = DataParser.parseTables()

app = App(domains)
app.mainloop()