from google import genai
import os


class AIAnalyzer:

    def __init__(self):
        key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key = key)

    def analyze(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text
    