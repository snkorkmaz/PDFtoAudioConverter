import shutil
import tkinter as tk
from tkinter import ttk, filedialog
import os
from pydub import AudioSegment
import pyttsx3
from PIL import Image, ImageTk
from customtkinter import CTkButton
from pdfreader import SimplePDFViewer
import pygame.mixer
import logging

# Initialize pygame.mixer
pygame.mixer.init()

# ---------------------------- CONSTANTS ------------------------------- #

BEIGE = "#FDF0D1"
DARK_PURPLE = "#643843"
MEDIUM_PURPLE = "#85586F"
LIGHT_PURPLE = "#AC7D88"
FONT_NAME = "Arial"
WAV_FILE_NAME = "./PDF_to_Speech.wav"
MP3_FILE_PATH = "./PDF_to_Speech.mp3"

# ------------------------ GLOBAL VARIABLES ----------------------------- #

pdf_file_path = ""
file_document = None
download_successful_label = None


# ---------------------------- FUNCTIONS ------------------------------- #

def center_window(window, width, height):
    """
        Centers the Tkinter window on the screen.
    """
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set window position
    window.geometry(f"{width}x{height}+{x}+{y}")

def get_text_from_pdf():
    """
        Retrieve text content from the PDF document.
    """
    global file_document
    viewer = SimplePDFViewer(file_document)
    viewer.render()
    string_list = viewer.canvas.strings
    final_text = ""
    for line in string_list:
        final_text += line + " "
    return final_text


def convert_text_to_speech():
    """
        Convert text from PDF to speech and save it as a WAV file.
    """
    text = get_text_from_pdf()
    engine = pyttsx3.init()
    engine.setProperty("voice", r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

    try:
        # Save text to speech as WAV
        engine.save_to_file(text, WAV_FILE_NAME)
        engine.runAndWait()

        # Show audio controls and hide convert button
        audio_image_canvas.grid(column=1, row=4, pady=20, rowspan=3)
        convert_button.grid_forget()
        play_button.grid(row=4, column=2)
        stop_button.grid(row=5, column=2)
        download_button.grid(row=6, column=2)
    except Exception as e:
        logging.error(f"Error occurred while saving speech to file: {e}")


def choose_filepath(event):
    """
        Open file dialog to choose PDF file path.
    """
    global pdf_file_path
    selected_filepath = filedialog.askopenfilename()
    if selected_filepath:
        file_path_entry_field.delete(0, tk.END)
        file_path_entry_field.insert(0, selected_filepath)
        pdf_file_path = selected_filepath


def upload_pdf():
    """
        Upload PDF file and display its icon.
    """
    global pdf_file_path, file_document
    if pdf_file_path:
        file_document = open(pdf_file_path, "rb")
        pdf_image_canvas.grid(column=1, row=1, pady=20)


def play_audio():
    """
        Play the audio from the WAV file.
    """
    sound = pygame.mixer.Sound(WAV_FILE_NAME)
    sound.play()


def stop_audio():
    """
        Stop the currently playing audio.
    """
    pygame.mixer.stop()


def convert_wav_to_mp3():
    """
        Convert the WAV file to MP3 format.
    """
    sound = AudioSegment.from_wav(WAV_FILE_NAME)
    sound.export(MP3_FILE_PATH, format="mp3")


def download():
    """
        Download the converted audio as an MP3 file.
    """
    global download_successful_label
    try:
        convert_wav_to_mp3()
        filename = os.path.basename(MP3_FILE_PATH)
        destination_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        destination_file_path = os.path.join(destination_dir, filename)
        shutil.copy2(MP3_FILE_PATH, destination_file_path)
        download_successful_label = tk.Label(text=f"Audio file downloaded to: Downloads", fg=DARK_PURPLE, bg=BEIGE,
                                             font=(FONT_NAME, 8))
        download_successful_label.grid(row=7, column=2)
        # delete the WAV and MP§ file after downloading
        # os.remove(WAV_FILE_NAME)
        # os.remove(MP3_FILE_PATH)
    except Exception as e:
        print(f"An error occurred during download: {e}")


# ---------------------------- UI SETUP ------------------------------- #

# CREATE A WINDOW
window = tk.Tk()
window.title("PDF To Speech Converter")
window.config(padx=25, pady=25, bg=BEIGE)
center_window(window, 800, 600)

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
