import DataStructures
import DataParser

import tkinter




domains = DataParser.parseTables()


class App:

    def __init__(self, master, data:[DataStructures.Domain]):
        frame = tkinter.Frame(master)
        frame.pack()

        self.buttons = []
        for domain in data:
            button = tkinter.Button(frame, text=domain.name, command= lambda domain=domain : self.printDomain(domain))
            button.pack(side=tkinter.TOP)
            self.buttons.append(button)

    def printDomain(self, domain:DataStructures.Domain):
        print("Domain name: " + domain.name)

        for library in domain.libraries:
            print("Domain contains library: " + library.name)



root = tkinter.Tk()

app = App(root, domains)

root.mainloop()


