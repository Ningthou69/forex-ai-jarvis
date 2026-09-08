#!/usr/bin/env python3
"""
JARVIS Voice Control - Main Entry Point
"""

from voice_jarvis import VoiceJarvis
import sys

def main():
    """Main voice mode launcher"""
    try:
        print("\n" + "="*60)
        print("  JARVIS VOICE MODE")
        print("="*60 + "\n")
        
        # Initialize voice JARVIS
        voice_jarvis = VoiceJarvis()
        
        # Test microphone
        if not voice_jarvis.test_microphone():
            print("Error: Microphone not available!")
            print("Install pyaudio: pip install pyaudio")
            sys.exit(1)
        
        # Start voice interaction
        voice_jarvis.start_voice_mode()
    
    except Exception as e:
        print(f"Fatal Error: {str(e)}")
        print("\nMissing dependencies? Install with:")
        print("pip install SpeechRecognition pyttsx3 pyaudio")
        sys.exit(1)

if __name__ == "__main__":
    main()