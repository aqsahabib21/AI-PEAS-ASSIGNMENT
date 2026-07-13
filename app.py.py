import os
import time
import speech_recognition as sr
import pyttsx3
from textblob import TextBlob

# Initialize Text-To-Speech (TTS Engine - Actuator)
engine = pyttsx3.init()
engine.setProperty('rate', 165)  # Humanized conversational pace

def speak(text):
    """Voice response synthesizer (TTS Actuator)"""
    print(f"Assistant (Voice Output): {text}")
    engine.say(text)
    engine.runAndWait()

class MultilingualVoiceAssistant:
    def __init__(self):
        self.conversation_history = []  # Tracks state (Sequential environment)
        self.mock_ticket_db = {}        # Mock Help-Desk Database API (Actuator)
        
        # Simple translation dictionary for localized demonstration (Multilingual)
        self.translations = {
            "hello": {"es": "hola", "ur": "salam", "en": "hello"},
            "help": {"es": "ayuda", "ur": "madad", "en": "help"},
            "refund": {"es": "reembolso", "ur": "refund", "en": "refund"},
            "status": {"es": "estado", "ur": "status", "en": "status"}
        }

    def detect_sentiment(self, text):
        """
        Calculates sentiment polarity (Sentiment Score Sensor/Process).
        Acts as an emotional-nuance inference model to balance partial observability.
        """
        analysis = TextBlob(text)
        score = analysis.sentiment.polarity
        if score > 0.1:
            return "Positive", score
        elif score < -0.1:
            return "Frustrated/Negative", score
        else:
            return "Neutral", score

    def listen_voice(self):
        """Uses speech recognition to process voice waveforms (Sensors)"""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("\n🎙️ Listening for customer input... (Background noise-cancellation active)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                print("⏳ Processing speech transcription...")
                # Multilingual Speech-to-Text translation simulation via Google Web Speech
                text = recognizer.recognize_google(audio)
                return text
            except sr.WaitTimeoutError:
                print("❌ Listening timed out.")
                return None
            except sr.UnknownValueError:
                print("❌ Could not understand audio waveforms.")
                return None
            except Exception as e:
                print(f"⚠️ System sensor failure: {e}")
                return None

    def process_customer_query(self, query):
        """Core AI Agent Decision Engine"""
        start_time = time.time()
        if not query:
            return "No input received.", 0, 0.0

        lowered_query = query.lower()
        sentiment, sentiment_val = self.detect_sentiment(lowered_query)
        self.conversation_history.append(lowered_query)

        # Basic natural language intent parsing (Multilingual)
        intent = "general_inquiry"
        if any(word in lowered_query for word in ["refund", "reembolso", "paisay"]):
            intent = "refund_request"
        elif any(word in lowered_query for word in ["status", "order", "delivery"]):
            intent = "order_status"
        elif any(word in lowered_query for word in ["agent", "human", "talk to representative"]):
            intent = "escalate"

        # Action/Response logic using the Utility Function:
        # Balanced logic: U = 0.6 * (Resolution_Quality) - 0.4 * (Wait_Time)
        response = ""
        resolved = True

        if intent == "refund_request":
            # Accessing Mock Database Actuator
            ticket_id = f"TKT-{int(time.time()) % 10000}"
            self.mock_ticket_db[ticket_id] = {"type": "Refund", "status": "Pending Verification"}
            response = f"I have processed your request and generated refund ticket {ticket_id}. Our team is reviewing it."
        elif intent == "order_status":
            response = "Your order status is currently shipped and is expected to arrive within 2 business days."
        elif intent == "escalate":
            response = "I am routing your call to a human support supervisor immediately."
            resolved = False
        else:
            response = "I understand. Let me help you with that inquiry. Could you provide your account number?"

        # Humanizing adaptations based on Sentiment Score
        if sentiment == "Frustrated/Negative":
            response = "I sincerely apologize for the inconvenience. " + response

        # Performance measurements calculation
        handling_time = round(time.time() - start_time, 2)
        
        return response, sentiment, handling_time, resolved

    def run_live_demo(self):
        """Starts the CLI and voice-controlled interactive loop"""
        speak("Hello! Thank you for contacting customer support. How can I assist you today?")
        
        while True:
            # Step 1: Sense input (Voice)
            user_input = self.listen_voice()
            
            # Text fallback to allow testing without a microphone setup
            if not user_input:
                user_input = input("\n📝 [Fallback Text Input] Type your query (or type 'exit'): ")
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                speak("Thank you for using our multilingual support. Goodbye!")
                break

            print(f"\n👤 Customer Spoke: \"{user_input}\"")

            # Step 2: Agent processes state and reasons
            response, sentiment, execution_time, resolved = self.process_customer_query(user_input)

            # Step 3: Actuate response (Voice and UI updates)
            print(f"--- [Real-Time Telemetry Logs] ---")
            print(f"📈 Sentiment Analyzed: {sentiment}")
            print(f"⏱️ Local Latency: {execution_time} seconds")
            print(f"✅ Issue Solved In-Agent: {resolved}")
            print(f"----------------------------------")
            
            speak(response)

if __name__ == "__main__":
    # Initialize and execute the virtual agent loop
    assistant = MultilingualVoiceAssistant()
    assistant.run_live_demo()