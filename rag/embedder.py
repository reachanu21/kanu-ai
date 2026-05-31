import requests

class LocalEmbedder:
    def __init__(self, host="http://localhost:11434", model="nomic-embed-text"):
        self.host = host
        self.model = model

    def embed(self, text):
        payload = {
            "model": self.model,
            "prompt": text
        }
        response = requests.post(f"{self.host}/api/embeddings", json=payload)
        response.raise_for_status()
        return response.json()["embedding"]
