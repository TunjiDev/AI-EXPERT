import speech_recognition as sr
import pyttsx3
from googletrans import Translator  # Google Translate API
import asyncio

# Initialize text-to-speech engine

def speak(text, language="en"):

    engine = pyttsx3.init()

    engine.setProperty('rate', 150)  # Speed of speech

    voices = engine.getProperty('voices')


    # Set voice for English or other language if supported by pyttsx3

    if language == "en":

        engine.setProperty('voice', voices[0].id)  # Default English voice

    else:

        engine.setProperty('voice', voices[1].id)  # Fallback to another voice if available    

    engine.say(text)

    engine.runAndWait()



# Speech-to-Text: Recognize spoken language (English)

def speech_to_text():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("???? Please speak now in English...")

        audio = recognizer.listen(source)


    try:

        print("???? Recognizing speech...")

        text = recognizer.recognize_google(audio, language="en-US")  # Use English for speech recognition

        print(f"✅ You said: {text}")

        return text

    except sr.UnknownValueError:

        print("❌ Could not understand the audio.")

    except sr.RequestError as e:

        print(f"❌ API Error: {e}")

    return ""


# Translate text using Google Translate API
async def translate_text(text, target_language="es"):
    async with Translator() as translator:
        translation = await translator.translate(
            text,
            dest=target_language
        )

        print(f"🌍 Translated text: {translation.text}")
        return translation.text



# Display language options to the user

def display_language_options():
   print("🌍 Available translation languages:")
   print("1. Spanish (es)")
   print("2. French (fr)")
   print("3. German (de)")
   print("4. Portuguese (pt)")
   print("5. Chinese - Simplified (zh-cn)")
   print("6. Japanese (ja)")
   print("7. Korean (ko)")
   print("8. Arabic (ar)")



    # User selects language

   choice = input("Please select the target language number (1-8): ")

   language_dict = {
      "1": "es",
      "2": "fr",
      "3": "de",
      "4": "pt",
      "5": "zh-cn",
      "6": "ja",
      "7": "ko",
      "8": "ar"
   }


   return language_dict.get(choice, "es")  # Default to Spanish if invalid input

# Main function to combine all steps
async def main():

    # Step 1: Display language options
    target_language = display_language_options()

    # Step 2: Speech-to-Text
    original_text = speech_to_text()

    if original_text:

        # Step 3: Translate text
        translated_text = await translate_text(
            original_text,
            target_language=target_language
        )

        # Step 4: Speak the original English text
        print("\nSpeaking original English text...")
        speak(original_text, language="en")

        # Step 5: Speak the translated text
        if translated_text:
            print("\nSpeaking translated text...")
            speak(translated_text, language=target_language)

            print("✅ Translation spoken out!")


if __name__ == "__main__":
    asyncio.run(main())