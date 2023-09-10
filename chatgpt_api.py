import openai
import speech_recognition as sr
from gtts import gTTS
import pyaudio
import subprocess
from playsound import playsound


# Set up your OpenAI API key
openai.api_key = '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'

# Function to interact with ChatGPT
def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()
 
# Function to convert text to speech and play it
def speak(text):
    myobj = gTTS(text=text, lang= 'en', slow=False)
    myobj.save('resp.mp3')
    playsound('resp.mp3')


# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Main loop for voice assistant
while True:
    try:
        with sr.Microphone() as source:
            print("Listening for a command...")
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()

            if 1==1:
                print("You said:", command)
                print("Processing...")
                response = chat_with_gpt(command)
                print("Arica:", response)
                speak(response)

    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Can you please repeat?")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
