from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

#funkcja otwierania programu oraz wyboru radiobuttons
def open_program():
    global filename
    #Okienko wyboru pliku
    filetypes = (('MOD', '*.MOD'), ('All files', '*.*'))
    filename = fd.askopenfilename(title='Otwórz plik', initialdir='/', filetypes=filetypes)
    showinfo(
        title='Plik otwarty!',
        message=filename
    )
    #Pobranie nazwy pliku
    name_to_split = filename.split('/')
    target_name = name_to_split[-1].split('.')
    #Pobranie nazwy stacji
    if int(target_name[0][1]) == 1:
        station_no = 'A2'
    elif int(target_name[0][1]) == 2:
        station_no = 'A1'
    #funkcja warunkowe przypisane do radiobuttons
    if selected() == 0:
        program_name_entry.insert(0, string=target_name[0])
        program_new_name.insert(0, string=target_name[0])
    elif selected() == 2:
        program_name_entry.insert(0, string=target_name[0])
        program_new_name.insert(0, string=station_no + target_name[0][2:len(target_name[0])])
    elif selected() == 1:
        program_name_entry.insert(0, string=target_name[0])
        program_new_name.insert(0, string='Part' + target_name[0][2:len(target_name[0])])

#funkcja zapisywania docelowego pliku
def save(final_file):
    filetypes = (('.MOD', '.MOD'), ('All files', '*.*'))
    new_file = fd.asksaveasfilename(title='Zapisz plik', initialdir='/', filetypes=filetypes)
    showinfo(
        title='Info',
        message='Plik zapisany!'
    )
    with open(new_file, 'w') as file:
        file.writelines(final_file)

#funkcja główna
def main_program():
    existing_name = program_name_entry.get()
    target_name = program_new_name.get()
    with open(filename, "r") as data_file:
        # tworzenie nowego programu z istniejącego na tej samej stacji
        if selected() == 0:
            program_name_entry.insert(0, string=existing_name)
            program_new_name.insert(0, string=target_name)
            data = data_file.read()
            first_rows = ['\nMODULE ' + existing_name[0:3] + target_name[3:(len(target_name))] + '\n\n      TASK PERS partdata pd_'+ existing_name[0:3] + target_name[3:(len(target_name))] + '_C:=["'+ existing_name[0:3] + target_name[3:(len(target_name))] + '_C","' + target_name[3:(len(target_name))] + '_C","",'+ existing_name[1] +',0,"","pdvProgStn'+ existing_name[1] +'"];\n']
            data = data.replace(existing_name, target_name)
            with open('XXXXX.MOD', 'w') as file:
                file.write(data)
            with open('XXXXX.MOD', 'r') as data_file_new:
                data = data_file_new.readlines()
                del data[0:4]
                save(final_file=first_rows+data)
        #tworzenie programu na innej stacji bazując na już istniejącym programie
        elif selected() == 2:
            program_name_entry.insert(0, string=existing_name)
            program_new_name.insert(0, string=target_name)
            data = data_file.read()
            data = data.replace(existing_name, target_name)
            if int(existing_name[1]) == 1:
                data = data.replace('",1,0,"","pdvProgStn1"', '",2,0,"","pdvProgStn2"')
                data = data.replace('obSide1', 'obSide2')
                data = data.replace('ActStn1', 'ActStn2')
            elif int(existing_name[1]) == 2:
                data = data.replace('",2,0,"","pdvProgStn2"', '",1,0,"","pdvProgStn1"')
                data = data.replace('obSide2', 'obSide1')
                data = data.replace('ActStn2', 'ActStn1')
            save(final_file=data)
        #tworzenie programu na dwie stacje jednocześnie, wybierając istniejący program z dowolnej stacji
        elif selected() == 1:
            program_name_entry.insert(0, string=existing_name)
            program_new_name.insert(0, string=target_name)
            data = data_file.read()
            first_rows = ['\nMODULE Part_' + existing_name[3:(
                len(existing_name))] + '\n\n      TASK PERS partdata pd_A1_' + existing_name[3:(
                len(existing_name))] + '_C:=["A1_' + existing_name[
                                                     3:(len(existing_name))] + '_C","' + existing_name[3:(
                len(existing_name))] + '_C","",1,0,"","pdvProgStn1"];\n      TASK PERS partdata pd_A2_' + existing_name[
                                                                                                          3:(
                                                                                                              len(existing_name))] + '_C:=["A2_' + existing_name[
                                                                                                                                                   3:(
                                                                                                                                                       len(existing_name))] + '_C","' + existing_name[
                                                                                                                                                                                        3:(
                                                                                                                                                                                            len(existing_name))] + '_C","",2,0,"","pdvProgStn2"];\n']
            if int(existing_name[1]) == 1:
                data = data.replace(existing_name, 'A2_' + existing_name[3:(len(existing_name))])
                data = data.replace('ENDMODULE', '')
                data = data.replace('MODULE ' + existing_name, 'MODULE ' + target_name)
                data = data.replace('obSide1', 'obSide2')
                data = data.replace('ActStn1', 'ActStn2')
            elif int(existing_name[1]) == 2:
                data = data.replace(existing_name, 'A1_' + existing_name[3:(len(existing_name))])
                data = data.replace('ENDMODULE', '')
                data = data.replace('MODULE ' + existing_name, 'MODULE ' + target_name)
                data = data.replace('obSide2', 'obSide1')
                data = data.replace('ActStn2', 'ActStn1')
            #zapis do pliku tymczasowego
            with open('XXXXX.MOD', 'w') as file:
                file.write(data)
            with open('XXXXX.MOD', 'r') as data_file_new:
                data = data_file_new.readlines()
            with open(filename, 'r') as data_file:
                new_data = data_file.readlines()
                no_of_rows = []
                #wyszukanie 'local pers' w istniejacym programie i usunięcie duplikatów
                for i in new_data:
                    if i.find('LOCAL PERS') != -1:
                        row_no = new_data.index(i)
                        no_of_rows.append(row_no)
                last_row = no_of_rows[-1]
                del new_data[0:last_row + 1]
                final_data = first_rows + data[4:len(data)] + new_data
                save(final_file=final_data)

#funkcja czyszcząca entry po przełaczeniu radiobuttons oraz zwrócenie wartosci danego radiobuttona
def selected():
    program_name_entry.delete(0, 'end')
    program_new_name.delete(0, 'end')
    return radio_state.get()



# UI config
window = Tk()
window.title('Copy robot program')
window.minsize(height=500, width=600)

canvas = Canvas(height=200, width=400)
logo_img = PhotoImage(file='Abb_logo_small.png')
canvas.create_image(200, 100, image=logo_img)
canvas.place(x=100, y=20)

# Buttons
open_file = Button(text='Otwórz plik:', width=60, command=open_program)
open_file.place(x=100, y=260)

save_file = Button(text='Zapisz plik', width=60, command=main_program)
save_file.place(x=100, y=380)

# Labels
existing_name = Label(text='Nazwa do zmiany:')
existing_name.place(x=100, y=300)

new_name = Label(text='Nowa nazwa:')
new_name.place(x=100, y=340)

# Entries
program_name_entry = Entry(width=45)
program_name_entry.place(x=250, y=300)

program_new_name = Entry(width=45)
program_new_name.place(x=250, y=340)

# Radio_button

radio_state = IntVar()
copy_program_station = Radiobutton(text='Kopiowanie na inną stacje', value=2, variable=radio_state, command=selected)
copy_program_station.place(x=210, y=220)

two_station_program = Radiobutton(text="Program na obie stacje", value=1, variable=radio_state, command=selected)
two_station_program.place(x=380, y=220)

new_program = Radiobutton(text='Nowy program', value=0, variable=radio_state, command=selected)
new_program.place(x=100, y=220)

window.mainloop()
