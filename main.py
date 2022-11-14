from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


def main_program():
    global filename
    filetypes = (('MOD', '*.MOD'), ('All files', '*.*'))
    filename = fd.askopenfilename(title='Otwórz plik', initialdir='/', filetypes=filetypes)
    showinfo(
        title='Plik otwarty!',
        message=filename
    )
    name_to_split = filename.split('/')
    name = name_to_split[-1].split('.')
    new_name = name[0]
    length = len(new_name)

    if int(new_name[1])==1:
        corect_no = 'A2'
    elif int(new_name[1])==2:
        corect_no = 'A1'

    if selected()==0:
        # print(name)
        program_name_entry.insert(0, string=name[0])
        program_new_name.insert(0,string=name[0])
    elif selected()==2:
        program_name_entry.insert(0, string=name[0])
        program_new_name.insert(0, string=corect_no+new_name[2:length])
    elif selected()==1:
        program_name_entry.insert(0, string=name[0])
        program_new_name.insert(0, string='Part'+new_name[2:length])

def save(final_line):
    filetypes = (('.MOD', '.MOD'), ('All files', '*.*'))
    new_file = fd.asksaveasfilename(title='Zapisz plik',initialdir='/',filetypes=filetypes)
    showinfo(
        title='Info',
        message='Plik zapisany!'
    )
    with open(new_file, 'w') as file:
        file.writelines(final_line)

def save_program():
    name = program_name_entry.get()
    new_name = program_new_name.get()
    with open(filename, "r") as data_file:
        if selected() == 0:
            line = data_file.read()
            line = line.replace(name, new_name)
            save(final_line=line)
        elif selected() == 2:
            line = data_file.read()
            line = line.replace(name,new_name)
            if int(name[1]) == 1:
                line = line.replace('",1,0,"","pdvProgStn1"', '",2,0,"","pdvProgStn2"')
                line = line.replace('obSide1', 'obSide2')
                line = line.replace('ActStn1', 'ActStn2')
            elif int(name[1]) == 2:
                line = line.replace('",2,0,"","pdvProgStn2"', '",1,0,"","pdvProgStn1"')
                line = line.replace('obSide2','obSide1')
                line = line.replace('ActStn2','ActStn1')
            save(final_line=line)
        elif selected() == 1:
            line = data_file.read()
            first_rows = ['\nMODULE Part_'+name[3:(len(name))]+'\n\n      TASK PERS partdata pd_A1_'+name[3:(len(name))]+'_C:=["A1_'+name[3:(len(name))]+'_C","'+name[3:(len(name))]+'_C","",1,0,"","pdvProgStn1"];\n      TASK PERS partdata pd_A2_'+name[3:(len(name))]+'_C:=["A2_'+name[3:(len(name))]+'_C","'+name[3:(len(name))]+'_C","",2,0,"","pdvProgStn2"];\n']
            if int(name[1]) == 1:
                line = line.replace(name, 'A2_'+name[3:(len(name))])
                line = line.replace('ENDMODULE', '')
                line = line.replace('MODULE ' + name, 'MODULE ' + new_name)
                line = line.replace('obSide1', 'obSide2')
                line = line.replace('ActStn1', 'ActStn2')

            elif int(name[1]) == 2:
                line = line.replace(name, 'A1_' + name[3:(len(name))])
                line = line.replace('ENDMODULE', '')
                line = line.replace('MODULE ' + name, 'MODULE ' + new_name)
                line = line.replace('obSide2','obSide1')
                line = line.replace('ActStn2','ActStn1')

            with open('XXXXX.MOD', 'w') as file:
                file.write(line)
            with open('XXXXX.MOD', 'r') as data_file_new:
                line = data_file_new.readlines()
            with open(filename, 'r') as data_file:
                new_line = data_file.readlines()
                new_index = []
                for i in new_line:
                    if i.find('LOCAL PERS') != -1:
                        # print('numer wiersza:', new_line.index(i))
                        # print(i)
                        n = new_line.index(i)
                        new_index.append(n)
                # print(new_index)
                naa = new_index[-1]
                del new_line[0:naa + 1]
                final_line = first_rows + line[4:len(line)] + new_line
                save(final_line=final_line)



def selected():
    program_name_entry.delete(0,'end')
    program_new_name.delete(0,'end')
    return radio_state.get()


#UI config
window = Tk()
window.title('Copy robot program')
window.minsize(height=500,width=600)

canvas = Canvas(height=200,width=400)
logo_img = PhotoImage(file='Abb_logo_small.png')
canvas.create_image(200,100,image=logo_img)
canvas.place(x=100,y=20)

#Buttons
open_file = Button(text='Otwórz plik:',width=60, command=main_program)
open_file.place(x=100,y=260)

save_file = Button(text='Zapisz plik',width=60, command=save_program)
save_file.place(x=100,y=380)

#Labels
existing_name = Label(text='Nazwa do zmiany:')
existing_name.place(x=100,y=300)

new_name = Label(text='Nowa nazwa:')
new_name.place(x=100,y=340)

#Entries
program_name_entry = Entry(width=45)
program_name_entry.place(x=250,y=300)

program_new_name = Entry(width=45)
program_new_name.place(x=250,y=340)

#Radio_button

radio_state = IntVar()
copy_program_station = Radiobutton(text='Kopiowanie na inną stacje',value=2,variable = radio_state, command = selected)
copy_program_station.place(x=210,y=220)

two_station_program = Radiobutton(text="Program na obie stacje",value=1,variable = radio_state, command = selected)
two_station_program.place(x=380,y=220)

new_program = Radiobutton(text='Nowy program',value=0,variable = radio_state, command = selected)
new_program.place(x=100,y=220)

window.mainloop()