import time

def speak(text):
    print(f"Assistant: {text}")

rclass MultilingualVoiceAssistant:
    def __init__(self):
        self.conversation_history = []
        self.mock_ticket_db = {}

        self.translations = {
            "hello": {"es": "hola", "ur": "salam", "en": "hello there"},
            "help": {"es": "ayuda", "ur": "madad", "en": "help me"},
            "refund": {"es": "reembolso", "ur": "refund", "en": "refund"},
            "status": {"es": "estado", "ur": "status", "en": "status"},
            "cancel": {"es": "cancelar", "ur": "cancel", "en": "cancel"}
        }

    def detect_sentiment(self, text):
        positive_words = ["good", "great", "thanks", "thank you", "excellent", "happy", "awesome"]
        negative_words = ["bad", "angry", "upset", "frustrated", "terrible", "hate", "not happy", "unhappy"]

        lower_text = text.lower()
        pos_score = sum(1 for word in positive_words if word in lower_text)
        neg_score = sum(1 for word in negative_words if word in lower_text)

        if pos_score > neg_score:
            return "Positive", pos_score - neg_score
        elif neg_score > pos_score:
            return "Frustrated/Negative", pos_score - neg_score
        return "Neutral", 0

    def listen_voice(self):
        try:
            return input("\nType your query (or type 'exit'): ").strip()
        except EOFError:
            return "exit"

    def process_customer_query(self, query):
        start_time = time.time()
        if not query:
            return "No input received.", "Neutral", 0.0, False

        lowered_query = query.lower()
        sentiment, sentiment_val = self.detect_sentiment(lowered_query)
        self.conversation_history.append(lowered_query)

        intent = "general_inquiry"
        if any(word in lowered_query for word in ["refund", "reembolso", "paisay"]):
            intent = "refund_request"
        elif any(word in lowered_query for word in ["status", "order", "delivery", "track"]):
            intent = "order_status"
        elif any(word in lowered_query for word in ["agent", "human", "talk to representative"]):
            intent = "escalate"
        elif any(word in lowered_query for word in ["cancel", "cancel order", "stop"]):
            intent = "cancel_order"

        response = ""
        resolved = True

        if intent == "refund_request":
            ticket_id = f"TKT-{int(time.time()) % 10000}"
            self.mock_ticket_db[ticket_id] = {"type": "Refund", "status": "Pending Verification"}
            response = f"I have processed your request and generated refund ticket {ticket_id}. Our team is reviewing it."
        elif intent == "order_status":   
            response = "Your order status is currently shipped and is expected to arrive within 2 business days."
        elif intent == "cancel_order":
            response = "I have initiated the cancellation of your order. You will recieve a confirmation email shortly."    
        elif intent == "escalate":
            response = "I am routing your call to a human support supervisor immediately."
            resolved = False
        else:
            response = "I understand. Let me help you with that inquiry. Could you provide your account number?"

        if sentiment == "Frustrated/Negative":
            response = "I sincerely apologize for the inconvenience. " + response

        handling_time = round(time.time() - start_time, 2)
        return response, sentiment, handling_time, resolved

    def run_live_demo(self):
        speak("Hello! Thank you for contacting customer support. How can I assist you today?")

        while True:
            user_input = self.listen_voice()

            if user_input.lower() in ['exit', 'quit', 'bye']:
                speak("Thank you for using our multilingual support. Goodbye!")
                break

            print(f"\nCustomer Typed: \"{user_input}\"")

            response, sentiment, execution_time, resolved = self.process_customer_query(user_input)

            print("--- [Real-Time Telemetry Logs] ---")
            print(f"Sentiment Analyzed: {sentiment}")
            print(f"Local Latency: {execution_time} seconds")
            print(f"Issue Solved In-Agent: {resolved}")
            print("----------------------------------")

            speak(response)

if __name__ == "__main__":
    assistant = MultilingualVoiceAssistant()
    assistant.run_live_demo