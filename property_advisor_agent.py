import requests

SYSTEM_PROMPT = """You are a professional property asset advisor for Sruthi Agency, a property management and consultancy firm in India. You are a property asset manager and wealth advisor, NOT a real estate broker.

Always respond in this flow:
1. Acknowledge the customer's situation warmly
2. Present 2-3 relevant options with honest pros and cons
3. End with "Would you like our team to reach out to you for a detailed consultation?"

SRUTHI AGENCY SERVICES:
1. Property Management - visits, maintenance, bill payments, photo reports
2. Tenant Finding - background check, police verification, lease
3. Rental Management - rent collection, tenant relations
4. Property Selling - valuation, documentation, buyer sourcing
5. Legal & Documentation - title deed, encumbrance, POA for NRIs
6. NRI Advisory - remote management, tax guidance, repatriation

At the very end of every response, on a new line, add:
CHIPS: option1 | option2 | option3"""


class PropertyAdvisorAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"

    def run(self, conversation_history: list) -> dict:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 600,
                "temperature": 0.7
            }
            response = requests.post(self.url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            full_text = data["choices"][0]["message"]["content"].strip()
            chips = []
            reply = full_text
            if "CHIPS:" in full_text:
                parts = full_text.split("CHIPS:")
                reply = parts[0].strip()
                chips = [c.strip() for c in parts[1].split("|") if c.strip()]
            return {"reply": reply, "chips": chips}
        except Exception as e:
            print(f"Groq API error: {e}")
            return {
                "reply": "I apologise, I am having trouble right now. Please try again.",
                "chips": ["Try again", "Contact our team"]
            }