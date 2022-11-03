from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

def open_program():
    global filename
    filetypes = (('text files','*.MOD'),('All files','*.*'))
    filename = fd.askopenfilename(title='Otwórz plik',initialdir='/',filetypes=filetypes)
    showinfo(
        title='Selected File',
        message=filename
    )
def read_program():
    name = program_name_entry.get()
    new_name = program_new_name.get()
    with open(filename, "r") as data_file:
        line = data_file.read()
        print(line)
        line = line.replace(name, new_name)
        print(line)
    filetypes = (('text files', '*.MOD'), ('All files', '*.*'))
    new_file = fd.asksaveasfilename(title='Zapisz plik',initialdir='/',filetypes=filetypes)
    showinfo(
        title='Info',
        message='Plik zapisany!'
    )
    with open(new_file, 'w') as file:
        file.write(line)



#UI config
window = Tk()
window.title('Copy robot program')
window.minsize(height=400,width=600)
# window.config(padx=100,pady=50)

canvas = Canvas(height=200,width=400)
logo_img = PhotoImage(file='Abb_logo_small.png')
canvas.create_image(200,100,image=logo_img)
canvas.place(x=100,y=20)

#Buttons
open_file = Button(text='Otwórz plik:',width=60, command=open_program)
open_file.place(x=100,y=220)

save_file = Button(text='Zapisz plik',width=60, command=read_program)
save_file.place(x=100,y=340)

#Labels
existing_name = Label(text='Podaj nazwę do zmiany:',)
existing_name.place(x=100,y=260)

new_name = Label(text='Podaj nową nazwę:')
new_name.place(x=100,y=300)

#Entries
program_name_entry = Entry(width=45)
program_name_entry.place(x=250,y=260)

program_new_name = Entry(width=45)
program_new_name.place(x=250,y=300)











window.mainloop()