from chatterbot import ChatBot
from tkinter import *
from googletrans import Translator, LANGUAGES
import speech_recognition as sr

translator = Translator()
bot = ChatBot("Oddy: The Bot")

def translate_to_destination(text, dest_language):
    if dest_language not in LANGUAGES.values():
        raise ValueError('Invalid destination language')
    translated = translator.translate(text, dest=dest_language)
    return translated.text

def ask_from_bot():
    query = textF.get()
    dest_language = destLangEntry.get()

    print("User Query:", query)
    print("Destination Language:", dest_language)

    try:
        # Get translation of user's query
        query_translated = translate_to_destination(query, dest_language)

        print("Translated Response:", query_translated)

        msgs.insert(END, "you : " + str(query) + "\n", 'user_message')
        msgs.insert(END, "bot : " + str(query_translated) + "\n", 'bot_message')  # Add "\n" for a new line

    except ValueError as e:
        msgs.insert(END, "Error: " + str(e))

    textF.delete(0, END)
    destLangEntry.delete(0, END)

def speech_to_text():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300  # Adjust this value if necessary
    with sr.Microphone() as source:
        print("Please speak now...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print("You said: " + query)
            textF.delete(0, END)
            textF.insert(0, query)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            msgs.insert(END, "Error: Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            msgs.insert(END, "Error: Could not request results from Google Speech Recognition service")

main = Tk()
main.geometry("500x650")
main.title("Oddy: The Bot")
main.configure(bg='lavender')

frame = Frame(main)
sc = Scrollbar(frame)
msgs = Text(frame, width=80, height=20, yscrollcommand=sc.set, font=("Verdana", 12))
sc.pack(side=RIGHT, fill=Y)
msgs.pack(side=LEFT, fill=BOTH, pady=10)
frame.pack()

# Add tags for user and bot messages
msgs.tag_configure('user_message', foreground='blue')
msgs.tag_configure('bot_message', foreground='#800080')  # Using hexadecimal color code for dark purple

queryLabel = Label(main, text="Translate this :", font=("Verdana", 14), fg='black', bg='lavender')
queryLabel.pack()

textF = Entry(main, font=("Verdana", 20))
textF.pack(fill=X, pady=10)

destLangLabel = Label(main, text="To :", font=("Verdana", 14), fg='black', bg='lavender')
destLangLabel.pack()

destLangEntry = Entry(main, font=("Verdana", 14))
destLangEntry.pack(fill=X, pady=5)

btn_frame = Frame(main)
btn_frame.pack(pady=10)

btn = Button(btn_frame, text="Translate", font=("Verdana", 20), command=ask_from_bot, fg='black', bg='#98FF98')
btn.pack(side=LEFT)

# Create a canvas for the circular button with more padding to the right
canvas = Canvas(btn_frame, width=50, height=50, bg='lavender', highlightthickness=0)
canvas.pack(side=LEFT, padx=10)

# Draw a circle on the canvas
circle = canvas.create_oval(5, 5, 45, 45, fill='#ADD8E6', outline='#ADD8E6')

# Bind the circle to the speech_to_text function
canvas.tag_bind(circle, '<Button-1>', lambda event: speech_to_text())

main.bind('<Return>', lambda event=None: btn.invoke())
main.mainloop()
