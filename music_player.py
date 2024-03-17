from tkinter import filedialog #importing the filediaglog module from the tkinter library
from tkinter import *   #importing all methods from the tkinter module
import pygame
import os

root = Tk()     #root object of the tk class
root.title("Music Player")
root.geometry("500x450")

pygame.mixer.init() #initializes pygame.mixer module for playing audio files


menubar = Menu(root) #add the Menu widget to the root window
root.config(menu=menubar) #Sconfigure the root window to use menubar as its menu bar, by setting the meny attribute of the root window to menubar


songs = []
current_song = ""
paused = False

#LOAD MUSIC INTO THE LISTBOX WIDGET
def load_music():
    global current_song
    root.directory = filedialog.askdirectory()  #prompt the user to select, a folder through a dialog box and then assigns the select path to the directory attribute of the root window.
                                                #filedialog module has askdirectory method; open dialog box and return the path.
    for song in os.listdir(root.directory): #os modules to work with files and directory, os.listdir list all the files and directories in the root.directory path
        name, ext = os.path.splitext(song)  #split the file name and its extension and return them as a tuple
        if ext == '.mp3':
            songs.append(song)
    
    for song in songs:
        songlist.insert("end", song) #insert song into listbox widget named songlist; "end" specifies where to insert the new item (the end of the list)
    
    songlist.selection_set(0) #selects the item at index 0 in the songlist listbox.
    current_song = songs[songlist.curselection()[0]] 
    
def play_music():
    global current_song, paused

    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song)) #load a song by giving the path to it, constructing the full path to the music file by joining the directory path and the file name
        pygame.mixer.music.play() #play the loaded music
    else:
        pygame.mixer.music.unpause() #when the music is currently paused, unpause the music and then set paused to False
        paused = False
    update_song_label()
def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True
def next_music():
    global current_song, paused
    
    try:
        songlist.selection_clear(0, END)  #clear the selection, no item in the listbox widget is selected
        songlist.selection_set(songs.index(current_song) + 1) #the song with index of current_song + 1 is selected
        current_song = songs[songlist.curselection()[0]] #update the current_song, curselection()[0] return the index of the first(only) selected item in the Listbox widget
        pygame.mixer.music.load(os.path.join(root.directory, current_song)) #load a song by giving the path to it, constructing the full path to the music file by joining the directory path and the file name
        pygame.mixer.music.play()
        update_song_label()
    except:
        pass

def prev_music():
    global current_song, paused

    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) - 1)
        current_song = songs[songlist.curselection()[0]] #curselection() is a method of the Listbox widget that returns a tuple containing the indices of the currently selected items
        pygame.mixer.music.load(os.path.join(root.directory, current_song)) #load a song by giving the path to it, constructing the full path to the music file by joining the directory path and the file name
        pygame.mixer.music.play()
        update_song_label()
    except:
        pass

def update_song_label():
    song_label.config(text=f"Now Playing: {current_song}                 ")

def move_text():
    
    formated_text = song_label.cget("text")
    text = formated_text[1:] + formated_text[0]
    song_label.config(text=text)
    song_label.after(300, move_text)

select_folder = Menu(menubar, tearoff=False) #create another menu object/widget winthin the menubar widget
select_folder.add_command(label='Select Folder', command=load_music) #adds a command to the Select Folder menu widget, this command is def load_music 
menubar.add_cascade(label='Get Music', menu=select_folder) #create a new menu item in the menubar Get Music with the label get Music , when this menu is clicked, it will display the select folder menu as a drop down



songlist = Listbox(root, bg="purple", fg="white", width=100, height=15) 
"""#root, place the listbox inside the root window, root is the name given to the main 
window of the tkinter application
widget_name = WidgetType(parent_window, additional_arguments)"""
songlist.pack()     #after creating the songlist widget variable, it's not display on the window, so we need to pack it
""".pack() display the widget on the window, automatically size and position widgets within their parent container"""



# Create a frame to contain the song title
song_frame = Frame(root, bg="lightgray", padx=10, pady=10)
song_frame.pack(fill="both", expand=True)

# Create a label to display the song title
song_label = Label(song_frame, text="Select a Folder and Press Play                 ", font=("Arial", 16), bg="lightgray")
song_label.pack(padx=10, pady=5)

play_btn_image = PhotoImage(file='play1.png') #PhotoImage is a class, PhotoImage(file='play.png') creates a PhotoImage object
next_btn_image = PhotoImage(file='next1.png')
pause_btn_image = PhotoImage(file='pause1.png')
prev_btn_image = PhotoImage(file='prev1.png')

control_frame = Frame(root, background="navy") #frame is like div in html, to orgaznie the widgets
control_frame.pack()

play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, command=play_music) #create the button widget, organize inside Frame widget
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, command=next_music)
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command=pause_music)
prev_btn = Button(control_frame, image=prev_btn_image, borderwidth=0, command=prev_music)

play_btn.grid(row=0, column=1, padx=10, pady=10)  #grid method position the widget within the parent container, row, colum, padx: padding, empty space left and right sides of the widget in pixels
next_btn.grid(row=0, column=3, padx=10, pady=10) #pady: padding, empty space to be added above and below the widget in pixel
pause_btn.grid(row=0, column=2, padx=10, pady=10)
prev_btn.grid(row=0, column=0, padx=10, pady=10)

move_text()
root.mainloop()     #Enter the main event loop of the GUI application, allowing it to handle events such as user interactions with the window
