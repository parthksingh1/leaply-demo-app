import os

# The app reads the key at import time; tests never call the real API.
os.environ.setdefault("OPENAI_API_KEY", "test-key")
