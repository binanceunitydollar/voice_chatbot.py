import os
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
import openai
from config import API_KEY


def listen():
    # Record audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        # Use Google Speech Recognition to convert speech to text
        text = r.recognize_google(audio)
        print("You: " + text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
    except sr.RequestError:
        print("Sorry, I couldn't request results from Google Speech Recognition.")


def speak(text):
    # Convert text to speech using gTTS
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    os.system('mpg321 output.mp3')


def search(query):
    # Perform a Google search and retrieve the top result
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all("div", class_="g")

    if search_results:
        result = search_results[0].find("div", class_="r").find("a").text
        return result
    else:
        return "No results found."


def generate_response(prompt):
    # Generate AI response using OpenAI's GPT-3.5 model
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()


# Load OpenAI API key from configuration file
openai.api_key = API_KEY


# Main program loop
while True:
    user_input = listen()
    if user_input:
        if "what is" in user_input.lower():
            query = user_input.lower().replace("what is", "").strip()
            result = search(query)
            print("AI: " + result)
            speak(result)
        else:
            prompt = "You said: " + user_input + "\nAI:"
            response = generate_response(prompt)
            print("AI: " + response)
            speak(response)
