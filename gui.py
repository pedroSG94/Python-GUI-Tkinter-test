from queue import Queue
from queue import Empty
from threading import Thread
from time import sleep
from tkinter import *
from custom_widgets import ROScrolledText


class MainWindows(Tk):

    def __init__(self):
        super().__init__()
        self.queue = Queue()

        self.geometry("300x200")
        self.title("Test")

        self.button = Button(text="Button", command=self.button_click)
        self.button.pack()

        self.scrolled_text = ROScrolledText()
        self.scrolled_text.pack()

    def button_click(self):
        self.button.configure(state=DISABLED)
        self.after(100, self.process_queue)
        ThreadedTask(self.queue).start()

    def process_queue(self):
        try:
            result = self.queue.get(0)
            if result == 0:
                self.button.configure(state=NORMAL)
            else:
                self.scrolled_text.insert(END, result + "\n")
                self.scrolled_text.see(END)
                self.after(100, self.process_queue)
        except Empty:
            self.after(100, self.process_queue)


class ThreadedTask(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        self.queue.put("working...")
        for i in range(20):
            sleep(0.5)
            self.queue.put("working... " + str(i))
        self.queue.put("finished!!!")
        self.queue.put(0)


main = MainWindows()
main.mainloop()
