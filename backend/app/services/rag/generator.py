# backend/app/services/rag/generator.py

from groq import Groq
from app.core.config import settings

print(" GENERATOR LOADED")

groq_client = Groq(api_key=settings.GROQ_API_KEY)


def groq_call(prompt: str):
    models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
    ]

    for model in models:
        try:
            print(f" Trying model: {model}")

            response = groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.choices[0].message.content

            # 🔥 EMPTY RESPONSE FIX
            if not content or not content.strip():
                print(f" Empty response from {model}")
                continue

            return content   # ✅ CORRECT POSITION

        except Exception as e:
            print(f" Model failed: {model} → {str(e)}")

    raise Exception("All Groq models failed")


def local_fallback(prompt: str):
    print(" Using local fallback")

    if "ai" in prompt.lower():
        return "Artificial Intelligence (AI) is the simulation of human intelligence in machines."

    return "AI system temporarily unavailable, but your data is loaded."


def generate_answer(prompt: str):
    print("🚀 GENERATE ANSWER START")

    try:
        answer = groq_call(prompt)

        # 🔥 DOUBLE SAFETY
        if not answer or not answer.strip():
            return local_fallback(prompt)

        return answer

    except Exception as e:
        print(" Groq completely failed:", str(e))
        return local_fallback(prompt)