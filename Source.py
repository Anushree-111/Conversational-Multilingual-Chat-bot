from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from tkinter import *
from googletrans import Translator, LANGUAGES
import speech_recognition as sr

translator = Translator()
bot = ChatBot("Oddy: The Bot")


# Function to train the bot with dialogues from a text file
def train_bot_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        dialogues = file.readlines()

    conversation = []
    for dialogue in dialogues:
        question, answer = dialogue.strip().split('\t')
        conversation.append(question)
        conversation.append(answer)

    trainer = ListTrainer(bot)
    trainer.train(conversation)


# Call the function to train the bot
train_bot_from_file(r"enter_file_path")


def translate_to_destination(text, dest_language):

    # Check if the destination language is valid
    if dest_language not in LANGUAGES.values():
        raise ValueError('Invalid destination language '+'\n')

    # Perform translation
    translated = translator.translate(text, dest=dest_language)
    return translated.text



def ask_from_bot():
    query = textF.get()
    dest_language = destLangEntry.get()

    print("User Query:", query)
    print("Destination Language:", dest_language)

    try:
        # Get response from the bot
        bot_response = bot.get_response(query).text

        # Translate bot's response to the destination language
        translated_response = translate_to_destination(bot_response, dest_language)

        print("Translated Response:", translated_response)

        msgs.insert(END, "you : " + str(query) + "\n", 'user_message')
        msgs.insert(END, "bot : " + str(translated_response) + "\n", 'bot_message')  # Display translated response

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
