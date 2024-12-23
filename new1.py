from tkinter import *
import pyttsx3
import datetime
import wikipedia
import webbrowser
import speech_recognition as sr

root = Tk()
root.title("AI Assistant")
root.geometry("1000x1000")
root.resizable(True, True)

text = None  # Initialize text variable
wished = False  # Boolean variable to track if wish has been made

def speak(audio):
    global text  # Use the global text variable
    if text:
        text.insert(END, audio + "\n")
        text.see(END)  # Scroll to the end of the text widget
        engine.say(audio)
        engine.runAndWait()

def wishme():
    global text, wished  # Use the global text variable and wished flag
    if text and not wished:
        hour = int(datetime.datetime.now().hour)
        if hour < 12:
            speak("Good morning Sohail Khan")
        elif 12 <= hour < 18:
            speak("Good afternoon Sohail Khan")
        else:
            speak("Good evening Sohail Khan")
        speak("Welcome aboard! I'm Friday, your virtual companion. Think of me as your tech-savvy wingman, ready to assist you in navigating the digital cosmos with style and flair.")
        wished = True  # Set wished flag to True after wishing

def takeCommand():
    global text  # Use the global text variable
    if text:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            speak("Listening...")
            text.update_idletasks()
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            speak("Recognizing...")
            text.update_idletasks()
            query = r.recognize_google(audio, language='en-in')
            text.insert(END, f"User said: {query}\n")
            text.see(END)  # Scroll to the end of the text widget
        except Exception as e:
            print(e)
            text.insert(END, "Say that again, please...\n")
            text.see(END)  # Scroll to the end of the text widget
            return "None"

        return query

def ask():
    global text  # Use the global text variable
    if text:
        wishme()  # Call wishme() function here
        query = takeCommand().lower()
        if 'exit' in query or 'stop' in query or 'quit' in query:
            text.insert(END, "Exiting Program...\n")
            speak("Sure, I'll stop now.")
            root.destroy()
        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            text.insert(END, "According to Wikipedia:\n")
            text.insert(END, results + "\n")
            text.see(END)  # Scroll to the end of the text widget
            speak(results)
        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com/")
        elif "open google chrome" in query:
            webbrowser.open("https://www.google.com/")
        elif "open gmail" in query:
            webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
        elif "what's the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            text.insert(END, f"Sir, the time is {strTime}\n")
            text.see(END)  # Scroll to the end of the text widget
            speak(f"Sir, the time is {strTime}")
        elif "what is today's date" in query:
            strDate = datetime.datetime.now().strftime("%d/%m/%Y")
            text.insert(END, f"Sir, today's date is {strDate}\n")
            text.see(END)  # Scroll to the end of the text widget
            speak(f"Sir, today's date is {strDate}")
        else:
            speak("Sorry, I didn't understand that.")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)

Label(root, text="AI assistant", font=("Comic Sans MS", 14, "bold")).place(x=180, y=20)

# Create a Text widget
text = Text(root, font=("Courier", 10), wrap=WORD, bg="lightblue")
text.place(x=70, y=100, width=900, height=500)

# Create a Scrollbar widget
scrollbar = Scrollbar(root, command=text.yview)
scrollbar.place(x=970, y=100, height=500)

# Configure the Text widget to use the Scrollbar
text.config(yscrollcommand=scrollbar.set)

Button(root, text="Ask", bg="lightblue", pady=16, padx=40, borderwidth=3, relief=SOLID, command=ask).place(x=90, y=620)

root.mainloop()
