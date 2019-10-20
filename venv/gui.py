from tkinter import *


class TradeMonitor:
    def __init__(self, parent):
        window = Tk()
        window.title('Trade Monitor')
        window.geometry('350x200')
        lbl = Label(window, text='Ask: ')
        lbl.grid(column=0, row=0)
        lbl2 = Label(window, text='0000.00')
        lbl2.grid(column=1, row=0)
        lbl3 = Label(window, text='Bid: ')
        lbl3.grid(column=0, row=1)
        lbl4 = Label(window, text='0000.00')
        lbl4.grid(column=1, row=1)

        def clicked():
            if btn.cget('text') == 'Run':
                btn.configure(text='End')
            elif btn.cget('text') == 'End':
                btn.configure(text='Run')

        btn = Button(window, text='Run', command=clicked)
        btn.grid(column=0, row=2)


def main():
    root = Tk()
    rw = TradeMonitor(root)
    root.mainloop()


if __name__ == '__main__':
    main()
