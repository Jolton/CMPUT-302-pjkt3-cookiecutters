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

        domianTabPage = DomainTabPage(container, self)
        domianTabPage.grid(row=0, column=0,sticky="nsew")
        self.frames[DomainTabPage] = domianTabPage


        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_domain(self, domain):
        frame = self.frames[DomainTabPage]
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


class DomainTabPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self)
        self.label.pack()

        self.controller = controller

        backButton = ttk.Button(self, text="Go Home", command = lambda : controller.show_frame(StartPage))
        backButton.pack()

        self.tabFrame = ttk.Notebook(self)
        self.tabFrame.pack()

        self.visualFrames = []

        popularityFrame = PopularityGraph(self.tabFrame)
        self.visualFrames.append(popularityFrame)
        self.tabFrame.add(popularityFrame, text='Compare Popularity')

        releaseFrame = ReleaseFrequencyGraph(self.tabFrame)
        self.visualFrames.append(releaseFrame)
        self.tabFrame.add(releaseFrame, text='Release Frequency')

        lastModifiedFrame = LastModifiedGraph(self.tabFrame)
        self.visualFrames.append(lastModifiedFrame)
        self.tabFrame.add(lastModifiedFrame, text='Last Modified')

        issuesFrame = IssuesGraph(self.tabFrame)
        self.visualFrames.append(issuesFrame)
        self.tabFrame.add(issuesFrame, text='Issues')



    def set_Domain(self, domain):
        self.domain = domain
        self.label.config(text=self.domain.name)
        for visual in self.visualFrames:
            visual.drawGraph(domain)







class VisualizationFrame(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.axis = self.figure.add_subplot(111)
        self.figure.subplots_adjust(bottom=0.5)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def drawGraph(self, domain):
        self.axis.clear()


class PopularityGraph(VisualizationFrame):

    def drawGraph(self, domain):
        super().drawGraph(domain)
        x = []
        heights = []
        names = []
        for i in range(len(domain.libraries)):
            x.append(i)
            heights.append(int(domain.libraries[i].popularity))
            names.append(domain.libraries[i].name)
        # print(x)
        # print(heights)
        # print(names)

        self.axis.bar(x, heights, tick_label=names)
        self.axis.tick_params(axis='x', labelrotation=45)

        self.canvas.draw()


class ReleaseFrequencyGraph(VisualizationFrame):

    def drawGraph(self, domain):
        super().drawGraph(domain)

        for library in domain.libraries:
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

            self.axis.plot_date(matplotlib.dates.date2num(years), counts, ls='solid', label=library.name)

        self.axis.tick_params(axis='x', labelrotation=45)
        self.axis.legend()
        self.canvas.draw()


class LastModifiedGraph(VisualizationFrame):

    def drawGraph(self, domain):
        super().drawGraph(domain)

        for library in domain.libraries:
            matdate = matplotlib.dates.date2num(library.lastModificationDate)
            self.axis.plot_date(matdate, [1], label=library.name)
            # self.axis.annotate(xy=(matdate, 1), s=library.name)
            # self.axis.axvline(matplotlib.dates.date2num(library.lastModificationDate))

        date = matplotlib.dates.date2num(datetime.date.today())
        self.axis.axvline(date,color='r')
        self.axis.text(date,1,"Today", rotation=90)
        # self.axis.legend(bbox_to_anchor=(0.7, -0.5))
        self.axis.tick_params(axis='x', labelrotation=45)
        self.axis.legend()
        self.axis.set_yticks([])
        self.canvas.draw()


class IssuesGraph(VisualizationFrame):

    def drawGraph(self, domain):
        super().drawGraph(domain)

        x = []
        genIssues = []
        secIssues = []
        perIssues = []
        secPlusPerIssues = []
        names = []
        i = -1
        for library in domain.libraries:
            i += 1
            x.append(i)
            names.append(library.name)
            genIssues.append(0)
            secIssues.append(0)
            perIssues.append(0)
            secPlusPerIssues.append(0)

            genCount = 0
            secCount = 0
            perCount = 0
            for issue in library.issues:
                if issue.security:
                    secCount += 1
                if issue.performance:
                    perCount += 1
                if not issue.security and not issue.performance:
                    genCount += 1

            total = genCount + secCount + perCount

            if total == 0:
                genIssues[i] = 0
                secIssues[i] = 0
                perIssues[i] = 0
            else:
                genIssues[i] = genCount / total * 100
                secIssues[i] = secCount / total * 100
                perIssues[i] = perCount / total * 100

            secPlusPerIssues[i] = secIssues[i] + perIssues[i]

        p1 = self.axis.bar(x, perIssues, tick_label=names)
        p2 = self.axis.bar(x, secIssues, bottom=perIssues)
        p3 = self.axis.bar(x, genIssues, bottom=secPlusPerIssues)
        self.axis.legend((p1[0], p2[0], p3[0]), ('Performance', 'Security', 'Generic'))

        self.axis.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter())
        self.axis.tick_params(axis='x', labelrotation=45)
        self.canvas.draw()






# old code
# class DomainPage(tk.Frame):
#
#     # self.colourButtonSelected =
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.label = tk.Label(self, text="Page Two")
#         self.label.pack(pady=10, padx=10, )
#
#         button1 = ttk.Button(self, text="Go Home", command = lambda: controller.show_frame(StartPage))
#         button1.pack()
#
#
#         settingFrame = tk.Frame(self)
#         settingFrame.pack()
#
#         self.settingButtons = {}
#
#         buttonComparePopularity = tk.Button(settingFrame, text="Popularity", command= lambda : self.compare_Popurarity())
#         buttonComparePopularity.pack(side=tk.LEFT)
#         self.settingButtons['buttonComparePopularity'] = buttonComparePopularity
#
#         buttonCompareRelease_Frequency = tk.Button(settingFrame, text="Release Frequency", command= lambda : self.compare_Release_Frequency())
#         buttonCompareRelease_Frequency.pack(side=tk.LEFT)
#         self.settingButtons['buttonCompareRelease_Frequency'] = buttonCompareRelease_Frequency
#
#         buttonCompareLast_Modification_Date = tk.Button(settingFrame, text="Last Modified", command = lambda : self.compare_Last_Modification())
#         buttonCompareLast_Modification_Date.pack(side=tk.LEFT)
#         self.settingButtons['buttonCompareLast_Modification_Date'] = buttonCompareLast_Modification_Date
#
#         buttonCompareIssues = tk.Button(settingFrame, text="Issues", command= lambda : self.compare_Issues())
#         buttonCompareIssues.pack(side=tk.LEFT)
#         self.settingButtons['buttonCompareIssues'] = buttonCompareIssues
#
#         buttonCompareSecurity = tk.Button(settingFrame, text="Set5")
#         buttonCompareSecurity.pack(side=tk.LEFT)
#         self.settingButtons['buttonCompareSecurity'] = buttonCompareSecurity
#
#
#         self.f = Figure(figsize=(5, 5), dpi=100)
#         self.axis = self.f.add_subplot(111)
#         self.f.subplots_adjust(bottom=0.5)
#
#         self.canvas = FigureCanvasTkAgg(self.f, self)
#         self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#
#         # self.canvas.draw()
#
#
#
#     def set_Domain(self, domain):
#         self.domain = domain
#
#         self.label.config(text=domain.name)
#
#         self.compare_Popurarity()
#
#
#     def compare_Popurarity(self):
#         self.select_button('buttonComparePopularity')
#
#         x = []
#         heights = []
#         names = []
#         for i in range(len(self.domain.libraries)):
#             x.append(i)
#             heights.append(int(self.domain.libraries[i].popularity))
#             names.append(self.domain.libraries[i].name)
#
#
#         self.axis.clear()
#
#         # print(x)
#         # print(heights)
#         # print(names)
#
#         self.axis.bar(x, heights, tick_label=names)
#         self.axis.tick_params(axis='x', labelrotation = 45)
#
#         self.canvas.draw()
#
#
#         # print(self.a.get_xticks())
#
#     def compare_Release_Frequency(self):
#         self.select_button('buttonCompareRelease_Frequency')
#
#         self.axis.clear()
#
#         for library in self.domain.libraries:
#             years = []
#             counts = []
#             for date in library.releaseDates:
#                 year = datetime.date(date.year, 1, 1)
#                 if year in years:
#                     index = years.index(year)
#                     counts[index] += 1
#                 else:
#                     years.append(year)
#                     counts.append(1)
#
#             self.axis.plot_date(matplotlib.dates.date2num(years), counts, ls='solid', label=library.name)
#
#         self.axis.legend()
#         self.canvas.draw()
#
#
#     def compare_Last_Modification(self):
#         self.select_button('buttonCompareLast_Modification_Date')
#
#         self.axis.clear()
#
#         for library in self.domain.libraries:
#             matdate = matplotlib.dates.date2num(library.lastModificationDate)
#             self.axis.plot_date(matdate, [1], label=library.name)
#             # self.axis.annotate(xy=(matdate, 1), s=library.name)
#             # self.axis.axvline(matplotlib.dates.date2num(library.lastModificationDate))
#
#         date = matplotlib.dates.date2num(datetime.date.today())
#         self.axis.axvline(date,color='r')
#         self.axis.text(date,1,"Today", rotation=90)
#         # self.axis.legend(bbox_to_anchor=(0.7, -0.5))
#         self.axis.legend()
#         self.axis.set_yticks([])
#         self.canvas.draw()
#
#
#     def compare_Issues(self):
#         self.select_button('buttonCompareIssues')
#
#         self.axis.clear()
#
#         x = []
#         genIssues = []
#         secIssues = []
#         perIssues = []
#         secPlusPerIssues = []
#         names = []
#         i = -1
#         for library in self.domain.libraries:
#             i += 1
#             x.append(i)
#             names.append(library.name)
#             genIssues.append(0)
#             secIssues.append(0)
#             perIssues.append(0)
#             secPlusPerIssues.append(0)
#
#             genCount = 0
#             secCount = 0
#             perCount = 0
#             for issue in library.issues:
#                 if issue.security:
#                     secCount += 1
#                 if issue.performance:
#                     perCount += 1
#                 if not issue.security and not issue.performance:
#                     genCount +=1
#
#             total = genCount + secCount + perCount
#
#             genIssues[i] = genCount / total * 100
#             secIssues[i] = secCount / total * 100
#             perIssues[i] = perCount / total * 100
#
#             secPlusPerIssues[i] = secIssues[i] + perIssues[i]
#
#
#
#
#         p1 = self.axis.bar(x, perIssues, tick_label=names)
#         p2 = self.axis.bar(x, secIssues, bottom=perIssues)
#         p3 = self.axis.bar(x, genIssues, bottom=secPlusPerIssues)
#         self.axis.legend((p1[0], p2[0], p3[0]), ('Performance', 'Security', 'Generic'))
#
#         self.axis.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter())
#         self.canvas.draw()
#
#
#
#
#
#     def select_button(self, buttonName):
#         """Sets only the given buttonName as disabled,(ie selected), and enables all the others"""
#         for button in self.settingButtons.values():
#             button.config(state=tk.ACTIVE)
#         self.settingButtons[buttonName].config(state=tk.DISABLED)


domains = DataParser.parseTables()

app = App(domains)
app.mainloop()