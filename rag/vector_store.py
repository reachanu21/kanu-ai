import faiss
import numpy as np
import json
import os

class VectorStore:
    def __init__(self, path="rag_index"):
        self.path = path
        self.index_file = f"{path}/index.faiss"
        self.meta_file = f"{path}/meta.json"

        os.makedirs(path, exist_ok=True)

        if os.path.exists(self.index_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.meta_file, "r") as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(768)  # embedding size
            self.metadata = []

    def add(self, embedding, text):
        vec = np.array([embedding]).astype("float32")
        self.index.add(vec)
        self.metadata.append(text)
        self._save()

    def search(self, embedding, k=5):
        vec = np.array([embedding]).astype("float32")
        distances, indices = self.index.search(vec, k)
        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results

    def _save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.meta_file, "w") as f:
            json.dump(self.metadata, f, indent=2)
