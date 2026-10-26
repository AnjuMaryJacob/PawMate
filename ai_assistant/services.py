import requests
import re

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"


def generate_pet_description(name, pet_type, breed, age, location, personality):
    prompt = f"""
You are writing a pet adoption listing for a website.

Pet details:
Name: {name}
Animal: {pet_type}
Breed: {breed or "Not specified"}
Age: {age}
Location: {location}
Personality: {personality or "Not specified"}

TASK:
Write one appealing pet adoption description of 80-120 words.

STRICT RULES:
- Start directly with the pet's description.
- Do not say "I'd be happy to", "Here is", "Here it is",
  "Sure", or "Of course".
- Do not include an introduction about writing the description.
- Do not repeat the instructions.
- Use only the information provided.
- Do not invent medical details or vaccination status.
- Encourage responsible adoption.
- Return only the final adoption description.
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 200
        }
    }

    try:
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()
        result = response.json()

        description = result.get("response", "").strip()

        # Remove common AI introductory phrases.
        description = re.sub(
            r"^(?:I'd be happy to(?:\s+\w+){0,6}\s*[,.:!-]?\s*|"
            r"I would be happy to(?:\s+\w+){0,6}\s*[,.:!-]?\s*|"
            r"Sure[,!]?\s*|"
            r"Of course[,!]?\s*|"
            r"Here(?:'s| is| it is)\s+"
            r"(?:(?:the|a)\s+)?"
            r"(?:pet adoption\s+)?description\s*[:\-]?\s*)",
            "",
            description,
            flags=re.IGNORECASE
        ).strip()

        # Remove quotation marks around the entire description.
        description = description.strip('"').strip("'").strip()

        if not description:
            raise ValueError("Ollama returned an empty description.")

        return description

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Cannot connect to Ollama. Make sure Ollama is running."
        ) from exc

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "Ollama took too long to respond. Please try again."
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Ollama request failed: {exc}"
        ) from exc

