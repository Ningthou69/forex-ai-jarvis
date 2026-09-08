#!/usr/bin/env python3
"""
JARVIS - AI Forex Trading Assistant
Main entry point for the application
"""

from jarvis import JarvisAI
import sys

def print_welcome():
    print("\n" + "="*60)
    print("  JARVIS - AI FOREX TRADING ASSISTANT")
    print("  Like Iron Man's JARVIS for Trading")
    print("="*60)
    print("\nCommands:")
    print("  'analyze' - Analyze forex pairs")
    print("  'geopolitical' - Check geopolitical news")
    print("  'system' - Get system information")
    print("  'clear' - Clear conversation history")
    print("  'exit' - Exit the program")
    print("\nOr just ask anything about forex trading!")
    print("-"*60 + "\n")

def main():
    """Main application loop"""
    try:
        # Initialize JARVIS
        jarvis = JarvisAI()
        print_welcome()
        
        # Main conversation loop
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    print("\nJARVIS: Goodbye, sir. It's been a pleasure.\n")
                    break
                
                if user_input.lower() == "clear":
                    jarvis.clear_history()
                    print("JARVIS: Conversation history cleared.\n")
                    continue
                
                # Process user message
                print("\nJARVIS: Processing...\n")
                response = jarvis.chat(user_input)
                print(f"JARVIS: {response}\n")
            
            except KeyboardInterrupt:
                print("\n\nJARVIS: Shutting down gracefully...\n")
                break
            except Exception as e:
                print(f"Error: {str(e)}\n")
    
    except Exception as e:
        print(f"Fatal Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()