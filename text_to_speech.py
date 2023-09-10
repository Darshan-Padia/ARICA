from gtts import gTTS
from playsound import playsound

class TextToSpeech:
    def __init__(self, name):
        self.name = name
        self.language = 'en'

    def convert_to_audio(self, output_file="welcome.mp3"):
        mytext = f'Welcome {self.name}. How may I help you?'
        myobj = gTTS(text=mytext, lang=self.language, slow=False)
        myobj.save(output_file)
        playsound(output_file)


# Example usage:
# if __name__ == "__main__":
#     name_to_greet = "John"
#     text_to_speech = TextToSpeech(name_to_greet)
#     text_to_speech.convert_to_audio()
