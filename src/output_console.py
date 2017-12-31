# GUI for Termi-Nalanda by cheese-cracker
from Tkinter import *


class display_box:
    def __init__(self, main):
        self.main = main
        self.title = main.title("\t\t***Nalanda***")
        self.text = "***Welcome to Nalanda Land***"
        self.label = Label(main, text=self.text)
        self.label.grid(row=1, column=1)

    def text_reset(self, new_output):
        self.text = new_output
        self.label.config(text=self.text)

    def text_add(self, next_line):
        self.text += "\n"
        self.text += next_line
        self.label.config(text=self.text)

    def dashify(self, upMainObj):
        self.u = upMainObj
        self.dashF = Frame(self.main)
        self.dashF.grid(row=1, column=2)
        self.c = {
            'notice': self.u.show_notice,
            'news': self.u.show_news,
            'lect': self.u.show_lect,
            'all': self.u.show_all,
        }
        self.noticebtn = Button(
            self.dashF, text="Notices!", command=self.c['notice'])
        self.noticebtn.pack()
        self.newsbtn = Button(self.dashF, text="News!", command=self.c['news'])
        self.newsbtn.pack()
        self.lecturesbtn = Button(
            self.dashF, text="Lectures!", command=self.c['lect'])
        self.lecturesbtn.pack()
        self.allbtn = Button(self.dashF, text="All", command=self.c['all'])
        self.allbtn.pack()


canvas = Tk()
display = display_box(canvas)
