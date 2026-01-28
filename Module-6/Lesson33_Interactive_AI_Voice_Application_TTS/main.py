import random
import time

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ Run: pip install pyttsx3")

def setup_tts():
    """Initialize text-to-speech"""
    if not TTS_AVAILABLE:
        return None
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 0.9)
        print("🔧 Engine initialized successfully")
        return engine
    except Exception as e:
        print(f"❌ TTS Setup Error: {e}")
        return None

def speak(engine, text):
    """Speak text or show fallback"""
    if engine is None:
        print(f"📝 [AUDIO]: {text}")
        return
    
    try:
        print(f"🔊 Speaking: {text}")
        # Don’t call engine.stop() here — it can interrupt ongoing speech
        engine.say(text)
        engine.runAndWait()  # Wait for the speech to finish
        print("✅ Speech completed")
    except Exception as e:
        print(f"❌ Speech Error: {e}")
        print(f"📝 [AUDIO]: {text}")

def get_samples():
    """Fun phrases to try"""
    return [
        "Hello! I am your computer!",
        "Python is awesome!",
        "This is AI speaking!",
        "Welcome to the future!"
    ]

def main():
    print("🎤 AI VOICE LAB")
    print("================")
    
    engine = setup_tts()
    
    if engine:
        print("✅ Voice ready! Try typing something...")
    else:
        print("⚠️ No audio, but you can still learn!")
        return
    
    speak(engine, "Hello! Type something for me to say!")
    time.sleep(0.2)  # Small pause after initial speech
    
    while True:
        try:
            text = input("\n💬 You: ").strip()
            
            if text.lower() == 'exit':
                speak(engine, "Goodbye!")
                break
            elif text.lower() == 'sample':
                phrase = random.choice(get_samples())
                print(f"🎯 Selected: {phrase}")
                speak(engine, phrase)
            elif text:
                speak(engine, text)
            else:
                print("💡 Type 'sample' for ideas or 'exit' to quit")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user")
            speak(engine, "Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break
    
    # Clean up
    try:
        if engine:
            engine.stop()
    except:
        pass
    
    print("\n👋 Program ended")

if __name__ == "__main__":
    main()



# import random
# import time

# try:
#     import pyttsx3
#     TTS_AVAILABLE = True
# except ImportError:
#     TTS_AVAILABLE = False
#     print("⚠️ Run: pip install pyttsx3")

# def setup_tts():
#     """Initialize text-to-speech"""
#     if not TTS_AVAILABLE:
#         return None
#     try:
#         engine = pyttsx3.init()
#         engine.setProperty("rate", 150)
#         engine.setProperty("volume", 0.9)
#         print("🔧 Engine initialized successfully")
#         return engine
#     except Exception as e:
#         print(f"❌ TTS Setup Error: {e}")
#         return None

# def speak(engine, text):
#     """Speak text or show fallback"""
#     if engine is None:
#         print(f"📝 [AUDIO]: {text}")
#         return
    
#     try:
#         print(f"🔊 Speaking: {text}")
#         # Clear any pending speech first
#         engine.stop()
#         # Add new speech
#         engine.say(text)
#         # Wait for it to complete
#         engine.runAndWait()
#         print("✅ Speech completed")
#     except Exception as e:
#         print(f"❌ Speech Error: {e}")
#         print(f"📝 [AUDIO]: {text}")
#         # Try to reinitialize engine if it failed
#         try:
#             engine = pyttsx3.init()
#             engine.setProperty("rate", 150)
#             engine.setProperty("volume", 0.9)
#         except:
#             pass

# def get_samples():
#     """Fun phrases to try"""
#     return [
#         "Hello! I am your computer!",
#         "Python is awesome!",
#         "This is AI speaking!",
#         "Welcome to the future!"
#     ]

# def main():
#     print("🎤 AI VOICE LAB")
#     print("================")
    
#     engine = setup_tts()
    
#     if engine:
#         print("✅ Voice ready! Try typing something...")
#     else:
#         print("⚠️ No audio, but you can still learn!")
#         return
    
#     speak(engine, "Hello! Type something for me to say!")
#     time.sleep(0.2)  # Small pause after initial speech
    
#     while True:
#         try:
#             text = input("\n💬 You: ").strip()
            
#             if text.lower() == 'exit':
#                 speak(engine, "Goodbye!")
#                 break
#             elif text.lower() == 'sample':
#                 phrase = random.choice(get_samples())
#                 print(f"🎯 Selected: {phrase}")
#                 speak(engine, phrase)
#             elif text:
#                 speak(engine, text)
#             else:
#                 print("💡 Type 'sample' for ideas or 'exit' to quit")
                
#         except KeyboardInterrupt:
#             print("\n\n👋 Interrupted by user")
#             speak(engine, "Goodbye!")
#             break
#         except Exception as e:
#             print(f"❌ Error: {e}")
#             break
    
#     # Clean up
#     try:
#         if engine:
#             engine.stop()
#     except:
#         pass
    
#     print("\n👋 Program ended")

# if __name__ == "__main__":
#     main()


# import random
# import time

# try:
#     import pyttsx3
#     TTS_AVAILABLE = True
# except ImportError:
#     TTS_AVAILABLE = False
#     print("⚠️ Run: pip install pyttsx3")

# # Global engine - initialize once
# engine = None

# def setup_tts():
#     """Initialize text-to-speech"""
#     global engine
#     if not TTS_AVAILABLE:
#         return None
#     try:
#         engine = pyttsx3.init()
#         engine.setProperty("rate", 150)
#         engine.setProperty("volume", 0.9)
#         print("🔧 Engine initialized successfully")
#         return engine
#     except Exception as e:
#         print(f"❌ TTS Setup Error: {e}")
#         return None

# def speak(text):
#     """Speak text or show fallback"""
#     global engine
#     if engine:
#         try:
#             print(f"🔊 Speaking: {text}")
#             engine.say(text)
#             engine.runAndWait()
#             time.sleep(0.1)  # Small delay to ensure completion
#             print("✅ Speech completed")
#         except Exception as e:
#             print(f"❌ Speech Error: {e}")
#             print(f"📝 [AUDIO]: {text}")
#     else:
#         print(f"📝 [AUDIO]: {text}")

# def get_samples():
#     """Fun phrases to try"""
#     return [
#         "Hello! I am your computer!",
#         "Python is awesome!",
#         "This is AI speaking!",
#         "Welcome to the future!"
#     ]

# def main():
#     print("🎤 AI VOICE LAB")
#     print("================")
    
#     tts_engine = setup_tts()
    
#     if tts_engine:
#         print("✅ Voice ready! Try typing something...")
#     else:
#         print("⚠️ No audio, but you can still learn!")
#         return
    
#     speak("Hello! Type something for me to say!")
    
#     while True:
#         text = input("\n💬 You: ").strip()
        
#         if text.lower() == 'exit':
#             speak("Goodbye!")
#             break
#         elif text.lower() == 'sample':
#             phrase = random.choice(get_samples())
#             print(f"🎯 Selected: {phrase}")
#             speak(phrase)
#         elif text:
#             speak(text)
#         else:
#             print("💡 Type 'sample' for ideas or 'exit' to quit")
    
#     print("\n👋 Program ended")

# if __name__ == "__main__":
#     main()

# import random

# try:
#     import pyttsx3
#     TTS_AVAILABLE = True
# except ImportError:
#     TTS_AVAILABLE = False
#     print("⚠️ Run: pip install pyttsx3")

# def setup_tts():
#     """Initialize text-to-speech"""
#     if not TTS_AVAILABLE:
#         return None
#     try:
#         engine = pyttsx3.init()
#         engine.setProperty("rate", 150)
#         engine.setProperty("volume", 0.9)
#         return engine
#     except:
#         return None

# def speak(engine, text):
#     """Speak text or show fallback"""
#     if engine:
#         try:
#             engine.say(text)
#             engine.runAndWait()
#         except:
#             print(f"???? [AUDIO]: {text}")
#     else:
#         print(f"???? [AUDIO]: {text}")

# def get_samples():
#     """Fun phrases to try"""
#     return [
#         "Hello! I am your computer!",
#         "Python is awesome!",
#         "This is AI speaking!",
#         "Welcome to the future!"
#     ]

# def main():
#     print("???? AI VOICE LAB")
#     print("================")
    
#     engine = setup_tts()
    
#     if engine:
#         print("✅ Voice ready! Try typing something...")
#     else:
#         print("⚠️ No audio, but you can still learn!")
    
#     speak(engine, "Hello! Type something for me to say!")
    
#     while True:
#         text = input("\n???? You: ").strip()
        
#         if text.lower() == 'exit':
#             speak(engine, "Goodbye!")
#             break
#         elif text.lower() == 'sample':
#             phrase = random.choice(get_samples())
#             print(f"???? {phrase}")
#             speak(engine, phrase)
#         elif text:
#             speak(engine, text)
#         else:
#             print("???? Type 'sample' for ideas or 'exit' to quit")

# if __name__ == "__main__":
#     main()


# ==========================================================================VERSION 1===============================================


# import speech_recognition as sr
# import pyttsx3
# from googletrans import Translator  # Google Translate API

# # Initialize text-to-speech engine
# def speak(text, language="en"):
#     engine = pyttsx3.init()
#     engine.setProperty('rate', 150)  # Speed of speech
#     voices = engine.getProperty('voices')
    
#     # Set voice for English or other language if supported by pyttsx3
#     if language == "en":
#         engine.setProperty('voice', voices[0].id)  # Default English voice
#     else:
#         engine.setProperty('voice', voices[1].id)  # Fallback to another voice if available
    
#     engine.say(text)
#     engine.runAndWait()

# # Speech-to-Text: Recognize spoken language (English)
# def speech_to_text():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("???? Please speak now in English...")
#         audio = recognizer.listen(source)
    
#     try:
#         print("???? Recognizing speech...")
#         text = recognizer.recognize_google(audio, language="en-US")  # Use English for speech recognition
#         print(f" ✅ You said: {text}")
#         return text
#     except sr.UnknownValueError:
#         print(" ❌ Could not understand the audio.")
#     except sr.RequestError as e:
#         print(f" ❌ API Error: {e}")
#         return ""

# # Translate text using Google Translate API
# def translate_text(text, target_language="es"):  # Default target language is Spanish (es)
#     translator = Translator()
#     translation = translator.translate(text, dest=target_language)
#     print(f"???? Translated text: {translation.text}")
#     return translation.text

# # Display language options to the user
# def display_language_options():
#     print("???? Available translation languages: ")
#     print("1. Hindi (hi)")
#     print("2. Tamil (ta)")
#     print("3. Telugu (te)")
#     print("4. Bengali (bn)")
#     print("5. Marathi (mr)")
#     print("6. Gujarati (gu)")
#     print("7. Malayalam (ml)")
#     print("8. Punjabi (pa)")
    
#     # User selects language
#     choice = input("Please select the target language number (1-8): ")
#     language_dict = {
#         "1": "hi",
#         "2": "ta",
#         "3": "te",
#         "4": "bn",
#         "5": "mr",
#         "6": "gu",
#         "7": "ml",
#         "8": "pa"
#     }
    
#     return language_dict.get(choice, "es")  # Default to Spanish if invalid input

# # Main function to combine all steps
# def main():
#     # Step 1: Display language options and get user's choice
#     target_language = display_language_options()
    
#     # Step 2: Speech-to-Text (recognizing English speech)
#     original_text = speech_to_text()
    
#     if original_text:
#         # Step 3: Translate to selected target language
#         translated_text = translate_text(original_text, target_language=target_language)
        
#         # Step 4: Text-to-Speech (Translate output and speak it)
#         speak(translated_text, language="en")  # Speak the translation in English
#         print(" ✅ Translation spoken out!")

# if __name__ == "__main__":
#     main()




# ==========================================================================VERSION 2===============================================
# import speech_recognition as sr
# import pyttsx3
# # from googletrans import Translator
# from deep_translator import GoogleTranslator

# # Initialize TTS engine once globally to avoid reinitialization issues
# engine = None

# def init_engine():
#     """Initialize the TTS engine once"""
#     global engine
#     if engine is None:
#         try:
#             engine = pyttsx3.init()
#             engine.setProperty('rate', 150)
#             # Test if engine works
#             print("✅ TTS Engine initialized successfully")
#         except Exception as e:
#             print(f"❌ Error initializing TTS engine: {e}")
#             print("Try: pip install --upgrade pyttsx3 pywin32 (on Windows)")
#     return engine

# def speak(text, language="en"):
#     """Text-to-speech function with error handling"""
#     try:
#         tts_engine = init_engine()
#         if tts_engine is None:
#             print("❌ TTS engine not available")
#             return
        
#         voices = tts_engine.getProperty('voices')
        
#         # Set voice for English or other language if supported by pyttsx3
#         if voices:
#             if language == "en":
#                 tts_engine.setProperty('voice', voices[0].id)
#             elif len(voices) > 1:
#                 tts_engine.setProperty('voice', voices[1].id)
        
#         print(f"🔊 Speaking: {text}")
#         tts_engine.say(text)
#         tts_engine.runAndWait()
#         print("✅ Speech completed")
        
#     except Exception as e:
#         print(f"❌ Error in speak function: {e}")
#         print("Possible fixes:")
#         print("  - Windows: pip install pywin32")
#         print("  - Linux: sudo apt-get install espeak")
#         print("  - Mac: TTS should work by default")

# def speech_to_text():
#     """Speech-to-text with error handling"""
#     recognizer = sr.Recognizer()
#     try:
#         with sr.Microphone() as source:
#             print("🎤 Please speak now in English...")
#             recognizer.adjust_for_ambient_noise(source, duration=0.5)
#             audio = recognizer.listen(source)
        
#         print("🔄 Recognizing speech...")
#         text = recognizer.recognize_google(audio, language="en-US")
#         print(f"✅ You said: {text}")
#         return text
        
#     except sr.UnknownValueError:
#         print("❌ Could not understand the audio.")
#         return ""
#     except sr.RequestError as e:
#         print(f"❌ API Error: {e}")
#         return ""
#     except Exception as e:
#         print(f"❌ Error: {e}")
#         return ""


# def translate_text(text, target_language="es"):
#     """Translate text using deep-translator"""
#     try:
#         translated = GoogleTranslator(source='en', target=target_language).translate(text)
#         print(f"📝 Translated text: {translated}")
#         return translated
#     except Exception as e:
#         print(f"❌ Translation error: {e}")
#         return text

# def display_language_options():
#     """Display language options to the user"""
#     print("\n🌐 Available translation languages:")
#     print("1. Hindi (hi)")
#     print("2. Tamil (ta)")
#     print("3. Telugu (te)")
#     print("4. Bengali (bn)")
#     print("5. Marathi (mr)")
#     print("6. Gujarati (gu)")
#     print("7. Malayalam (ml)")
#     print("8. Punjabi (pa)")
    
#     choice = input("\nPlease select the target language number (1-8): ")
#     language_dict = {
#         "1": "hi", "2": "ta", "3": "te", "4": "bn",
#         "5": "mr", "6": "gu", "7": "ml", "8": "pa"
#     }
    
#     return language_dict.get(choice, "es")

# def test_tts():
#     """Test TTS functionality"""
#     print("\n🧪 Testing TTS...")
#     speak("Hello, this is a test of the text to speech system.")

# def main():
#     print("=" * 50)
#     print("SPEECH TRANSLATOR")
#     print("=" * 50)
    
#     # Test TTS first
#     test_tts()
    
#     # Step 1: Display language options and get user's choice
#     target_language = display_language_options()
    
#     # Step 2: Speech-to-Text (recognizing English speech)
#     original_text = speech_to_text()
    
#     if original_text:
#         # Step 3: Translate to selected target language
#         translated_text = translate_text(original_text, target_language=target_language)
        
#         # Step 4: Text-to-Speech (Translate output and speak it)
#         if translated_text:
#             speak(translated_text, language="en")
#             print("✅ Translation spoken out!")
#     else:
#         print("❌ No text to translate")

# if __name__ == "__main__":
#     main()



# ==========================================================================VERSION 3===============================================
# import speech_recognition as sr
# import pyttsx3
# from googletrans import Translator

# # Initialize TTS engine globally to avoid reinitialization issues
# engine = None

# def init_engine():
#     """Initialize the TTS engine once"""
#     global engine
#     if engine is None:
#         engine = pyttsx3.init()
#         engine.setProperty('rate', 150)
#     return engine

# def speak(text, language="en"):
#     """Text-to-speech function"""
#     try:
#         tts_engine = init_engine()
#         voices = tts_engine.getProperty('voices')
        
#         # Set voice
#         if language == "en" and voices:
#             tts_engine.setProperty('voice', voices[0].id)
#         elif len(voices) > 1:
#             tts_engine.setProperty('voice', voices[1].id)
        
#         print(f"🔊 Speaking: {text}")
#         tts_engine.say(text)
#         tts_engine.runAndWait()
        
#     except Exception as e:
#         print(f"❌ Speech error: {e}")

# def speech_to_text():
#     """Speech-to-text: Recognize spoken English"""
#     recognizer = sr.Recognizer()
#     try:
#         with sr.Microphone() as source:
#             print("🎤 Please speak now in English...")
#             recognizer.adjust_for_ambient_noise(source, duration=0.5)
#             audio = recognizer.listen(source, timeout=10)
        
#         print("🔄 Recognizing speech...")
#         text = recognizer.recognize_google(audio, language="en-US")
#         print(f"✅ You said: {text}")
#         return text
        
#     except sr.UnknownValueError:
#         print("❌ Could not understand the audio.")
#         return ""
#     except sr.RequestError as e:
#         print(f"❌ API Error: {e}")
#         return ""
#     except Exception as e:
#         print(f"❌ Error: {e}")
#         return ""

# def translate_text(text, target_language="es"):
#     """Translate text using Google Translate API"""
#     try:
#         translator = Translator()
#         translation = translator.translate(text, dest=target_language)
        
#         # Extract translated text
#         translated_text = translation.text if hasattr(translation, 'text') else str(translation)
        
#         print(f"📝 Original: {text}")
#         print(f"📝 Translated ({target_language}): {translated_text}")
#         return translated_text
        
#     except Exception as e:
#         print(f"❌ Translation error: {e}")
#         print("Returning original text...")
#         return text

# def display_language_options():
#     """Display language options to the user"""
#     print("\n🌐 Available translation languages:")
#     print("1. Hindi (hi)")
#     print("2. Tamil (ta)")
#     print("3. Telugu (te)")
#     print("4. Bengali (bn)")
#     print("5. Marathi (mr)")
#     print("6. Gujarati (gu)")
#     print("7. Malayalam (ml)")
#     print("8. Punjabi (pa)")
    
#     choice = input("\nPlease select the target language number (1-8): ")
#     language_dict = {
#         "1": "hi",
#         "2": "ta",
#         "3": "te",
#         "4": "bn",
#         "5": "mr",
#         "6": "gu",
#         "7": "ml",
#         "8": "pa"
#     }
    
#     selected = language_dict.get(choice, "hi")
#     print(f"✅ Selected language: {selected}")
#     return selected

# def main():
#     print("=" * 60)
#     print("SPEECH TRANSLATOR - English to Indian Languages")
#     print("=" * 60)
    
#     # Step 1: Display language options and get user's choice
#     target_language = display_language_options()
    
#     # Step 2: Speech-to-Text (recognizing English speech)
#     original_text = speech_to_text()
    
#     if original_text:
#         # Step 3: Translate to selected target language
#         translated_text = translate_text(original_text, target_language=target_language)
        
#         # Step 4: Text-to-Speech (speak the translated text)
#         if translated_text:
#             speak(translated_text, language=target_language)
#             print("✅ Translation spoken out!")
#         else:
#             print("❌ No translation to speak")
#     else:
#         print("❌ No text captured from speech")
    
#     print("\n" + "=" * 60)

# if __name__ == "__main__":
#     main()