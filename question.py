import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "https://api.hku.hk/openai/student/deployments/gpt-4.1-mini/chat/completions?api-version=2025-04-01-preview"

def generate_questions(text, max_text_length=6000, num_questions=5):
    if len(text) > max_text_length:
        text = text[:max_text_length] + "\n...[truncated due to length]"

    prompt = f"""
    You are an examiner. 
    Your job is to set {num_questions} high-quality examination question-answer pairs based on the lecture notes.
    Return ONLY valid JSON in this exact format.

    {{
    "topic": "brief topic name",
    "qa_pairs": [
        {{"question": "question 1", "answer": "answer 1"}},
        {{"question": "question 2", "answer": "answer 2"}}
    ]
    }}
    
    EXAMPLE FORMAT:

    {{
    "topic": "Module 5 Embedded System Hardware",
    "qa_pairs": [
        {{"question": "Why cannot we ignore hardware when designing embedded systems?", "answer": "Because hardware affects real-time behavior, efficiency, energy consumption, security, and reliability."}},
        {{"question": "What is the main difference between CCD and CMOS image sensors?", "answer": "CCD sensors are optimized for optics with serial access and lower power consumption, while CMOS sensors use standard VLSI technology with random access and higher power consumption."}}
    ]
    }}

    REAL TEXT TO ANALYZE:
    {text}
    """

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    data = {
        "messages": [
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 1500, #response length
        "temperature": 0.3, #creativity
        "top_p": 0.95 #diversity
    }

    try:
        response = requests.post(URL, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            return ai_response
        else:
            return f"API Error: {response.status_code}\n{response.text}"

    except requests.exceptions.Timeout:
        return "Error: API request timed out."
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to HKU API."
    except Exception as e:
        return f"Unexpected error: {str(e)}"

