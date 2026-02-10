import os
import json
import re
from google import genai


class NLPClient:
    def __init__(self):
        # Try environment variable first
        api_key = os.getenv("GEMINI_API_KEY")

        # Fallback: local file (safe for demo)
        if not api_key:
            try:
                with open("config/gemini_key.txt", "r") as f:
                    api_key = f.read().strip()
            except Exception:
                raise RuntimeError(
                    "Gemini API key not found. "
                    "Set GEMINI_API_KEY or add key to config/gemini_key.txt"
                )

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-1.5-flash"

    def parse(self, user_input: str):
        prompt = f"""
You are a drone operations coordinator AI.

Extract intent and entities from the command below.

Command:
"{user_input}"

Return ONLY valid JSON with keys:
intent, priority, location, mission_id

Rules:
- intent: query | query_pilots | query_drones | assign | reassign
- priority: urgent | normal
- use null if missing
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            text = response.text.strip()
            text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)

        except Exception:
            # Safe deterministic fallback
            return {
                "intent": "reassign"
                if "reassign" in user_input.lower()
                else "assign"
                if "assign" in user_input.lower()
                else "query",
                "priority": "urgent"
                if "urgent" in user_input.lower()
                else "normal",
                "location": None,
                "mission_id": self._extract_mission_id(user_input),
            }

    def _extract_mission_id(self, text: str):
        match = re.search(r"M\d+", text, re.IGNORECASE)
        return match.group().upper() if match else None
