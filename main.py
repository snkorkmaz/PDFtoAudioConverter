import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from customtkinter import CTkButton
import pygame.mixer

# Initialize pygame.mixer
pygame.mixer.init()

# ---------------------------- CONSTANTS ------------------------------- #

BEIGE = "#FDF0D1"
DARK_PURPLE = "#643843"
MEDIUM_PURPLE = "#85586F"
LIGHT_PURPLE = "#AC7D88"
FONT_NAME = "Arial"

# ---------------------------- FUNCTIONS ------------------------------- #
def get_text_from_pdf():
    pass


def convert_text_to_speech():
    pass


def choose_filepath(event):
    pass


def upload_pdf():
    pass


def play_audio():
    pass


def stop_audio():
    pass


def convert_wav_to_mp3():
    pass


def download():
    pass


# ---------------------------- UI SETUP ------------------------------- #

# CREATE A WINDOW
window = tk.Tk()
window.title("PDF To Speech Converter")
window.geometry("800x600")
window.config(padx=25, pady=25, bg=BEIGE)

# CREATE CUSTOM STYLE FOR ENTRY WIDGET
style = ttk.Style()
style.configure('Custom.TEntry', bordercolor=DARK_PURPLE, relief='solid', fieldbackground='white',
                foreground="black", padding=5, focuscolor=MEDIUM_PURPLE)

# CREATE HEADER LABEL
heading = tk.Label(text="Convert a PDF File to Speech", fg=DARK_PURPLE, bg=BEIGE, font=(FONT_NAME, 35, "bold"))
heading.grid(column=1, row=0, columnspan=4, pady=50)

# CREATE PDF ICON
pdf_icon = Image.open("static/assets/img/PDF_file_icon.png")
pdf_icon = pdf_icon.resize((100, 100), Image.Resampling.LANCZOS)
pdf_icon = ImageTk.PhotoImage(pdf_icon)

# CREATE CANVAS TO DISPLAY PDF ICON
pdf_image_canvas = tk.Canvas(window, width=100, height=100, bg=BEIGE, highlightthickness=0)
pdf_image_canvas.create_image(0, 0, anchor='nw', image=pdf_icon)

# CREATE ENTRY FIELD FOR CHOOSING THE FILE PATH
file_path_entry_field = ttk.Entry(window, width=50, style='Custom.TEntry')
file_path_entry_field.grid(row=3, column=1, padx=10, pady=10)

# BIND choose_filepath FUNCTION TO ENTRY FIELD
file_path_entry_field.bind("<Button-1>", choose_filepath)

# UPLOAD BUTTON
pdf_upload_button = CTkButton(window, command=upload_pdf, text="Upload")
pdf_upload_button.configure(text_color="white", fg_color=MEDIUM_PURPLE, bg_color=BEIGE, hover_color=LIGHT_PURPLE,
                            corner_radius=50, width=220,
                            font=(FONT_NAME, 15, "bold"))
pdf_upload_button.grid(row=3, column=2)

# CONVERT BUTTON
convert_button = CTkButton(window, text="Convert")
convert_button.configure(text_color="white", fg_color=MEDIUM_PURPLE, bg_color=BEIGE, hover_color=LIGHT_PURPLE,
                         corner_radius=50, width=220, command=convert_text_to_speech,
                         font=(FONT_NAME, 15, "bold"))
convert_button.grid(row=4, column=2)

# CREATE AUDIO ICON
audio_icon = Image.open("static/assets/img/sound-wave-equalizer.png")
audio_icon = audio_icon.resize((300, 100), Image.Resampling.LANCZOS)
audio_icon = ImageTk.PhotoImage(audio_icon)

# CREATE CANVAS TO DISPLAY AUDIO ICON
audio_image_canvas = tk.Canvas(window, width=300, height=100, bg=BEIGE, highlightthickness=0)
audio_image_canvas.create_image(0, 0, anchor='nw', image=audio_icon)

# PLAY BUTTON
play_symbol = u"\u25B6"  # Unicode for the play symbol
play_button = CTkButton(window, text=f"{play_symbol}  Play Audio", command=play_audio)
play_button.configure(text_color="white", fg_color=MEDIUM_PURPLE, bg_color=BEIGE, hover_color=LIGHT_PURPLE,
                      corner_radius=50, width=220, font=(FONT_NAME, 15, "bold"))

# STOP BUTTON
stop_symbol = u"\u25A0"  # Unicode for the stop symbol
stop_button = CTkButton(window, text=f"{stop_symbol}  Stop Audio", command=stop_audio)
stop_button.configure(text_color="white", fg_color=MEDIUM_PURPLE, bg_color=BEIGE, hover_color=LIGHT_PURPLE,
                      corner_radius=50, width=220, font=(FONT_NAME, 15, "bold"))

# DOWNLOAD BUTTON
download_symbol = u"\u2B73"  # Unicode for the download symbol
download_button = CTkButton(window, text=f"{download_symbol}  Download", command=download)
download_button.configure(text_color="white", fg_color=MEDIUM_PURPLE, bg_color=BEIGE, hover_color=LIGHT_PURPLE,
                          corner_radius=50, width=220, font=(FONT_NAME, 15, "bold"))

window.mainloop()
