import pyttsx3
import PyPDF2
from tkinter import *
from tkinter.filedialog import *
import tkinter.messagebox
import customtkinter
import speech_recognition as sr
import keyboard
import pywhatkit as pw

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

global go,count
go=1
count = 1

class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("AudioBook")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        self.var1 = IntVar(value=100)
        self.var2 = tkinter.IntVar()
        global r,g,book,pages,pdfreadder
        r=50
        g=0
        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="AudioBook",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.slider = customtkinter.CTkSlider(master=self.frame_left,
                                                from_=50,
                                                to=250,
                                                variable=self.var1)
        self.slider.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Set the rate of words",
                                                command=self.setrate)
        self.button_1.grid(row=4, column=0, pady=10, padx=10)

        self.label_2 = customtkinter.CTkLabel(master=self.frame_left,
                                                text="100" ,
                                                corner_radius=6,  # <- custom corner radius
                                                fg_color=("white", "gray38"),  # <- custom tuple-color
                                                justify=tkinter.CENTER)
        self.label_2.grid(row=3, column=0, sticky="nwe", padx=15, pady=15)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        self.inpvariable: tkinter.Variable = None
        self.input = customtkinter.CTkEntry(master=self.frame_right, textvariable=self.inpvariable)
        self.input.grid(row=5,column=0,columnspan=2, pady=10, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Video",
                                                command=self.ytsearch)
        self.button_5.grid(row=5, column=0, pady=10, padx=20)


        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Select file to be read:" ,
                                                   height=150,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)


        # ============ frame_right ============

        self.button_2 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Open PDF File",
                                                command=self.browse)
        self.button_2.grid(row=4, column=0, pady=10, padx=20)

        self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Select voice:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, pady=20, padx=10, sticky="")

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.var2,
                                                           text="Male",
                                                           value=0,
                                                           command=self.gender)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.var2,
                                                           text="Female",
                                                           value=1,
                                                           command=self.gender)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        self.button_3 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Play",
                                                command=self.play)
        self.button_3.grid(row=8, column=2, pady=10, padx=20)

        self.button_4 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Stop",
                                                command=self.pause)
        self.button_4.grid(row=9, column=2, pady=10, padx=20)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Save as MP3 file",
                                                command=self.save_mp3)
        self.button_5.grid(row=10, column=2, pady=10, padx=20)

        # self.button_6 = customtkinter.CTkButton(master=self.frame_left,
        #                                         text="mic",
        #                                         command=self.speechtotext)
        # self.button_6.grid(row=5, column=0, pady=10, padx=20)



        # set default values
        self.optionmenu_1.set("Dark")
        self.radio_button_1.select()

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

    def setrate(self):
        global r
        r = self.var1.get()
        self.label_2.set_text(r)

    def gender(self):
        global g
        g= self.var2.get()

    def browse(self):
        global book,pages,pdfreadder
        book = askopenfilename()
        pdfreadder = PyPDF2.PdfFileReader(book)
        pages = pdfreadder.numPages
    
    def play(self):
        for num in range(0, pages):
            page = pdfreadder.getPage(num)
            text = page.extractText().replace('\n\n', '*newline*')\
            .replace('\n', ' ')\
            .replace('*newline*', '\n\n')
            player = pyttsx3.init()
            rate = player.getProperty('rate')
            player.setProperty('rate', r)
            voices = player.getProperty('voices')
            player.setProperty('voice', voices[g].id)
            player.say(text)
            player.runAndWait()
        self.button_3.configure(state="disabled")


    def pause(self):
        #code to pause
        self.button_4.configure(state="disabled")
   
    def save_mp3(self):
        global count
        saveastext=''
        pdfreadder11 = PyPDF2.PdfFileReader(book)
        pages = pdfreadder11.numPages
        for num in range(0,pages):
        
            page = pdfreadder.getPage(num)
            text = page.extractText().replace('\n\n', '*newline*')\
            .replace('\n', ' ')\
            .replace('\n\n\n',' ')\
            .replace('*newline*', '\n\n')
            engine=pyttsx3.init()
            rate = engine.getProperty('rate')
            engine.setProperty('rate', r)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[g].id)
            saveastext+=text
        print(saveastext)
        engine.save_to_file(text= saveastext,filename='your recording' + str(count) + '.mp3')
        count+=1
        engine.runAndWait()

    def speechtotext(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # read the audio data from the default microphone
            audio_data = r.record(source, duration=5)
            print("Recognizing...")
            # convert speech to text
            text = r.recognize_google(audio_data)
            print(text)
    
    def ytsearch(self):
        search_var = self.inpvariable
        pw.playonyt(search_var)

    
if __name__ == "__main__":
    app = App()
    app.mainloop()