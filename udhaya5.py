import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googletrans import Translator
import requests
import json

r = sr.Recognizer()
engine = pyttsx3.init()
translator = Translator()

def take_command():
    speak("Listening...")
    with sr.Microphone() as source:
        audio = r.listen(source)
        speak("Recognizing...")
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            speak("Sorry, I didn't understand that,Say that again please sir.")
            print(e)
            return "None"
    return query

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def send_email(to, subject, message):
    speak("Please enter your email password")
    password = input("Enter your email password: ")
    msg = MIMEMultipart()
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(msg['From'], password)
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()

def translate_text(text, dest_language):
    result = translator.translate(text, dest=dest_language)
    speak(f"The translation is: {result.text}")

def get_weather(city):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    weather_data = response.json()
    speak(f"The weather in {city} is {weather_data['weather'][0]['description']}. The temperature is {weather_data['main']['temp']} Kelvin.")

def get_news():
    api_key = "YOUR_NEWSAPI_API_KEY"
    base_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(base_url)
    news_data = response.json()
    speak("Here are the top headlines:")
    for article in news_data['articles']:
        speak(article['title'])

def main():
    while True:
        query = take_command().lower()
        
        if 'hello' in query:
            speak("Hello! How are you?")
        elif 'how are you' in query:
            speak("I'm good, thanks!")
        elif 'what is your name' in query:
            speak("My name is Jarvis")
        elif 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif 'what is the date' in query:
            today = datetime.date.today()
            speak(today.strftime("Today's date is %D"))
        elif 'search wikipedia' in query:
            speak("What do you want to search sir?")
            search_query = take_command()
            results = wikipedia.summary(search_query, sentences=2)
            speak("According to the search, ")
            speak(results)
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
            speak("Google is open")
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
            speak("YouTube is open")
        elif 'open tinkercad' in query:
            webbrowser.open("https://www.tinkercad.com")
            speak("Tinkercad is open")
        elif 'open whatsapp' in query:
            webbrowser.open("https://www.whatsapp.com")
            speak("Whatsapp is open")
        elif 'send email' in query:
            speak("Who do you want to send the email to?")
            to = take_command()
            speak("What is the subject of the email?")
            subject = take_command()
            speak("What is the message of the email?")
            message = take_command()
            send_email(to, subject, message)
        elif 'translate text' in query:
            speak("What is the text you want to translate?")
            text = take_command()
            speak("What is the destination language?")
            dest_language = take_command()
            translate_text(text, dest_language)
        elif 'get weather' in query:
            speak("Which city's weather do you want to know?")
            city = take_command()
            get_weather(city)
        elif 'get news' in query:
            speak("Here are the top headlines:")
            get_news()
        elif 'exit' in query:
            speak("Goodbye! sir")
            break

if __name__ == "__main__":
    main()