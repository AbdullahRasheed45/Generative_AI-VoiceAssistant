import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS

print("perfect!!")
load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY



def voice_input():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, timeout=15, phrase_time_limit=15)

    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio")
        return ""  # Return an empty string instead of None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service: {e}")
        return ""  # Return an empty string instead of None

    

def text_to_speech(text):
    tts=gTTS(text=text, lang="en")
    
    #save the speech from the given text in the mp3 format
    tts.save("speech.mp3")

def llm_model_object(user_text):
    #model = "models/gemini-pro"
    
    genai.configure(api_key=GOOGLE_API_KEY)
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    response=model.generate_content(user_text)
    
    result=response.text
    
    return result
    