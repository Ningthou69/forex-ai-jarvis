import speech_recognition as sr
import pyttsx3
from jarvis import JarvisAI
import threading
import sys

class VoiceJarvis:
    """Voice-enabled JARVIS AI Assistant"""
    
    def __init__(self):
        self.jarvis = JarvisAI()
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.tts_engine = pyttsx3.init()
        
        # Configure text-to-speech
        self.tts_engine.setProperty('rate', 150)  # Speed
        self.tts_engine.setProperty('volume', 0.9)  # Volume
        
        self.listening = True
        self.microphone = sr.Microphone()
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"\nJARVIS: {text}\n")
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")
    
    def listen(self):
        """Listen for voice commands"""
        try:
            with self.microphone as source:
                print("\nJARVIS: Listening...\n")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=10)
            
            # Recognize speech using Google Speech Recognition
            print("JARVIS: Processing speech...\n")
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}\n")
            return text
        
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you repeat?")
            return None
        except sr.RequestError as e:
            self.speak(f"Error with speech recognition: {e}")
            return None
        except sr.Timeout:
            self.speak("I didn't hear anything. Please try again.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def process_voice_command(self, command):
        """Process voice command and respond"""
        if not command:
            return
        
        # Handle special commands
        if "exit" in command.lower() or "quit" in command.lower():
            self.speak("Goodbye, sir. It's been a pleasure.")
            self.listening = False
            return
        
        if "clear" in command.lower():
            self.jarvis.clear_history()
            self.speak("Conversation history cleared.")
            return
        
        if "stop listening" in command.lower():
            self.speak("Stopping voice mode.")
            self.listening = False
            return
        
        # Process with JARVIS
        print("JARVIS: Processing your request...\n")
        try:
            response = self.jarvis.chat(command)
            self.speak(response)
        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            print(error_msg)
            self.speak("Sorry, I encountered an error. Please try again.")
    
    def start_voice_mode(self):
        """Start voice interaction loop"""
        self.print_welcome()
        
        while self.listening:
            try:
                # Listen for command
                command = self.listen()
                
                if command:
                    # Process command
                    self.process_voice_command(command)
            
            except KeyboardInterrupt:
                print("\n\nShutting down...")
                self.speak("Shutting down gracefully.")
                self.listening = False
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def print_welcome(self):
        """Print welcome message"""
        print("\n" + "="*60)
        print("  JARVIS - VOICE-ENABLED AI FOREX ASSISTANT")
        print("="*60)
        print("\nVoice Commands:")
        print("  'analyze EUR_USD' - Analyze a forex pair")
        print("  'geopolitical' - Check geopolitical news")
        print("  'system info' - Get system information")
        print("  'clear' - Clear conversation")
        print("  'exit' or 'quit' - Exit program")
        print("\nOr just speak naturally!")
        print("-"*60)
        print("\nInitializing microphone...\n")
        self.speak("JARVIS online. Ready to assist with forex trading.")
    
    def test_microphone(self):
        """Test microphone connection"""
        try:
            with self.microphone as source:
                print("Testing microphone...")
                audio = self.recognizer.listen(source, timeout=2)
                print("Microphone working!\n")
                return True
        except Exception as e:
            print(f"Microphone error: {e}")
            return False