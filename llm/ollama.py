import requests

class OllamaLLM:
    def __init__(self, model="llama3.2", host="http://localhost:11434", mode="Balanced"):
        self.model = model
        self.host = host
        self.mode = mode

    def temperature(self):
        return {
            "Balanced": 0.5,
            "Creative": 0.9,
            "Precise": 0.2
        }.get(self.mode, 0.5)

    def generate(self, prompt, temperature=None):
        # If no temperature override is provided, use mode-based temperature
        if temperature is None:
            temperature = self.temperature()

        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }

        response = requests.post(f"{self.host}/api/generate", json=payload)
        response.raise_for_status()

        data = response.json()
        return data.get("response", "")
