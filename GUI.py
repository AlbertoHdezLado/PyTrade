from tkinter import *
from tkinter import ttk, font, PhotoImage

from ExtractData import ExtractData


class GUI(ttk.Frame):
    extractor = ExtractData()

    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.window = Tk()
        self.window.title("PyTrade 1.0")
        self.window.geometry('1280x720')
        self.window.configure(bg='#e1e9f4')
        self.window.resizable(0, 0)


        # DEFINE MENU BAR:
        menu_bar = Menu(self.window)
        self.window['menu'] = menu_bar

        # DEFINE SUBMENUS:
        menu1 = Menu(menu_bar)
        menu2 = Menu(menu_bar)
        menu3 = Menu(menu_bar)
        menu_bar.add_cascade(menu=menu1, label='Functions')
        menu_bar.add_cascade(menu=menu2, label='Options')
        menu_bar.add_cascade(menu=menu3, label='Help')

        # DEFINE FUNCTIONS:
        menu1.add_command(label='F1', command=self.market,
                          underline=0, accelerator="Ctrl+c",
                          compound=LEFT)
        menu1.add_separator()  # Agrega un separador
        menu1.add_command(label='Salir', command=self.exit,
                          underline=0, accelerator="Ctrl+q",
                          compound=LEFT)

        #
        coinsMarket = self.extractor.getCoinsMarket()
        self.table = ttk.Treeview(self.window, column=('#1', '#2', '#3'))
        # self.table.grid(row=4, column=0, columnspan=1)
        self.table.heading("#0", text='Image', anchor='center')
        self.table.heading("#1", text='Name', anchor='center')
        self.table.heading("#2", text='Image', anchor='center')
        self.table.heading("#3", text='Name', anchor='center')

        style = ttk.Style(self.window)
        style.configure("Treeview", rowheight=100, anchor='center')

        for i in range(len(coinsMarket)):
            # coinImage = PhotoImage(Image.open(requests.get(coinsMarket[i]['image'], stream=True).raw))
            self._img = PhotoImage(file="Imagenes\\dados.png")

            # self.table.insert(parent='', index='end', iid=i, Image=coinImage, value=(coinsMarket[i]['id'], coinsMarket[i]['image'], 0))
            self.table.insert('', 'end', text="#0's text", image=self._img,
                              values=("A's value", "B's value"))

        self.table.pack()

        # VISUALIZE
        #self.market()
        self.window.mainloop()

    # DEFINE METHODS:
    def market(self):
        coinsMarket = self.extractor.getCoinsMarket()
        self.table = ttk.Treeview(self.window, column=('#1', '#2', '#3'))
        #self.table.grid(row=4, column=0, columnspan=1)
        self.table.heading("#0", text='Image', anchor='center')
        self.table.heading("#1", text='Name', anchor='center')
        self.table.heading("#2", text='Image', anchor='center')
        self.table.heading("#3", text='Name', anchor='center')

        style = ttk.Style(self.window)
        style.configure("Treeview", rowheight=100, anchor='center')
        self._img = PhotoImage(file="Imagenes\dados.png")
        for i in range(len(coinsMarket)):
            #coinImage = PhotoImage(Image.open(requests.get(coinsMarket[i]['image'], stream=True).raw))


            #self.table.insert(parent='', index='end', iid=i, Image=coinImage, value=(coinsMarket[i]['id'], coinsMarket[i]['image'], 0))
            self.table.insert('', 'end', text="#0's text", image=self._img,
                                 values=("A's value", "B's value"))

        self.table.pack()

            #print
            #vent2.insert(self.extractor.getCoinsMarket()[coin]['id'],coin, 1)


    def exit(self):
        self.window.destroy()




def main():
    mi_app = GUI()
    return 0


if __name__ == '__main__':
    root = Tk()
    root.geometry('450x180+300+300')

    app = GUI(root)
    app.grid(row=0, column=0, sticky='nsew')

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    root.mainloop()
