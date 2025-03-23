# pip install gtts deep-translator

from gtts import gTTS
from deep_translator import GoogleTranslator
import os

# Function to convert text to Hindi speech
def text_to_speech_hindi(text, file_name="output.mp3"):
    # Translate text to Hindi
    translated_text = GoogleTranslator(source="en", target="hi").translate(text)
    
    # Convert translated text to speech
    tts = gTTS(text=translated_text, lang="hi", slow=False)
    tts.save(file_name)

    return file_name  # Return file name for playback
