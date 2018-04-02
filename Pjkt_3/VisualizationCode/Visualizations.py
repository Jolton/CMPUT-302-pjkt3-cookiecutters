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
        label = tk.Label(self, text="Pick a domain to compare libraries")
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

        issuesFrame = IssueTypeGraph(self.tabFrame)
        self.visualFrames.append(issuesFrame)
        self.tabFrame.add(issuesFrame, text='Issues Types')

        issuesResponseTime = IssueResponseTimeGraph(self.tabFrame)
        self.visualFrames.append(issuesResponseTime)
        self.tabFrame.add(issuesResponseTime, text='Issue Response time')

        issuesClossingTime = IssueClosingTimeGraph(self.tabFrame)
        self.visualFrames.append(issuesClossingTime)
        self.tabFrame.add(issuesClossingTime, text='Issue Closing time')

        breakingChangesFrame = BackwardsCompatibilityGraph(self.tabFrame)
        self.visualFrames.append(breakingChangesFrame)
        self.tabFrame.add(breakingChangesFrame, text='Backwards Compatibility')

        stackOverflowFrame = StackOverflowGraph(self.tabFrame)
        self.visualFrames.append(stackOverflowFrame)
        self.tabFrame.add(stackOverflowFrame, text='Stack Overflow')


    def set_Domain(self, domain):
        self.domain = domain
        self.label.config(text='Comparing libraries for: ' + self.domain.name)
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

        self.axis.set_title(label="The number of projects that use each library")
        self.axis.set_ylabel('Number of projects')
        self.axis.set_xlabel('Libraries')

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

        self.axis.set_title(label='The number of releases per year for each library')
        self.axis.set_ylabel('Number of releases')
        self.axis.set_xlabel('Time')
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

        self.axis.set_title('The last time each library was modified')
        self.axis.set_xlabel("Time")
        self.axis.legend()
        self.axis.set_yticks([])
        self.canvas.draw()


class IssueTypeGraph(VisualizationFrame):

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

        self.axis.set_title('Types of Issues per library')
        self.axis.set_ylabel('Percent of the total issues')
        self.axis.set_xlabel('Libraries')
        self.canvas.draw()


class IssueResponseTimeGraph(VisualizationFrame):
    """Draws a side by side bar graph showing the average response time and
    the number of unanswered issues per library"""

    def __init__(self, parent):
        VisualizationFrame.__init__(self, parent)

        self.twinAxis = self.axis.twinx()

    def drawGraph(self, domain):
        super().drawGraph(domain)

        xTicks = []
        names = []
        numberUnanswered = []
        averageResponseTime = []

        for libIndex in range(len(domain.libraries)):
            xTicks.append(libIndex)
            names.append(domain.libraries[libIndex].name)

            numberUnanswered.append(0)
            averageResponseTime.append(0)

            responseTimes = []
            for issue in domain.libraries[libIndex].issues:
                if issue.firstCommentDate == None:
                    numberUnanswered[libIndex] += 1
                else:
                    responseTimes.append(issue.firstCommentDate - issue.creationDate)

            total = datetime.timedelta()
            for time in responseTimes:
                total += time

            if len(responseTimes) != 0:
                ave = total / len(responseTimes)
                averageResponseTime[libIndex] = ave.seconds/86400


        width = 0.4
        self.axis.tick_params(axis='x', labelrotation=45)
        self.twinAxis.clear()

        p1 = self.axis.bar(xTicks, averageResponseTime, width=-width, align='edge', color='b', tick_label=names)
        self.axis.set_ylabel("Response Time (Days)")
        p2 = self.twinAxis.bar(xTicks, numberUnanswered, width=width, align='edge', color='r')
        self.twinAxis.set_ylabel("Unanswered Issues")
        self.twinAxis.legend((p1,p2), ('Average Reponse Time', 'Number of Unanswered issues'))
        self.axis.set_title('Average time to respond to issues and the number of issues that have no response')
        self.axis.set_xlabel('Libraries')

        self.canvas.draw()


class IssueClosingTimeGraph(VisualizationFrame):


    def __init__(self, parent):
        VisualizationFrame.__init__(self, parent)

        self.twinAxis = self.axis.twinx()

    def drawGraph(self, domain):
        super().drawGraph(domain)

        self.twinAxis.clear()

        xTicks = []
        names = []
        numberOpen = []
        averageClosingTime = []

        for libIndex in range(len(domain.libraries)):
            xTicks.append(libIndex)
            names.append(domain.libraries[libIndex].name)

            numberOpen.append(0)
            averageClosingTime.append(0)

            responseTimes = []
            for issue in domain.libraries[libIndex].issues:
                if issue.closingDate == None:
                    numberOpen[libIndex] += 1
                else:
                    responseTimes.append(issue.closingDate - issue.creationDate)

            total = datetime.timedelta()
            for time in responseTimes:
                total += time

            if len(responseTimes) != 0:
                ave = total / len(responseTimes)
                averageClosingTime[libIndex] = ave.seconds / 86400

        width = 0.4
        self.axis.tick_params(axis='x', labelrotation=45)

        p1 = self.axis.bar(xTicks, averageClosingTime, width=-width, align='edge', color='b', tick_label=names)
        self.axis.set_ylabel("Closing Time (Days)")
        p2 = self.twinAxis.bar(xTicks, numberOpen, width=width, align='edge', color='r')
        self.twinAxis.set_ylabel("Open Issues")
        self.twinAxis.legend((p1, p2), ('Average Closing Time', 'Number of Open issues'))
        self.axis.set_title('Average time to close an issue and the number of open issues')
        self.axis.set_xlabel('Libraries')

        self.canvas.draw()


class BackwardsCompatibilityGraph(VisualizationFrame):

    def drawGraph(self, domain):
        super().drawGraph(domain)

        xTicks = []
        breakingChanges = []
        names = []

        for idx, library in enumerate(domain.libraries):
            xTicks.append(idx)
            names.append(library.name)
            breakingChanges.append(0)

            for (release, changes) in library.breakingChangesPerRelease:
                # print(library.name)
                # print(str(release) + '|' + str(changes))
                breakingChanges[idx] += changes

            breakingChanges[idx] = breakingChanges[idx] / len(library.breakingChangesPerRelease)

        self.axis.bar(xTicks, breakingChanges, tick_label=names)
        self.axis.set_ylabel('Average Breaking changes')
        self.axis.set_title('The average number of breaking changes per release')
        self.axis.set_xlabel('Libraries')

        self.canvas.draw()


class StackOverflowGraph(VisualizationFrame):

    def drawGraph(self, domain):
        super().drawGraph(domain)

        for library in domain.libraries:
            if library.lastDiscussedOnStackOverflow != 'Never':

                self.axis.plot_date(matplotlib.dates.date2num(library.lastDiscussedOnStackOverflow), [int(library.questionsAsked)] ,label= library.name)

        today = matplotlib.dates.date2num(datetime.date.today())
        self.axis.axvline(today, color='r')

        (min, max) = self.axis.get_ylim()
        mid = (max - min)/2  + min

        self.axis.text(today, mid,  'Today', rotation= 90)
        self.axis.tick_params(axis='x', labelrotation=45)
        self.axis.set_title('The last time a library was disused on stack overflow and the number of questions asked about it')
        self.axis.set_ylabel('The number of questions')
        self.axis.set_xlabel('Time last discussed on stack overflow')
        self.axis.legend()
        self.canvas.draw()




domains = DataParser.parseTables()

app = App(domains)
app.mainloop()