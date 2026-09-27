import base64
import json
from openai import OpenAI
from django.conf import settings


def analyze_environment_image(image_path):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    prompt = """
Sen EcoAI ekologik sun'iy intellekt yordamchisisan.

Berilgan rasmni ekologik nuqtai nazardan tahlil qil.

Faqat JSON formatida javob ber.

JSON quyidagi ko'rinishda bo'lsin:

{
    "problem": "asosiy ekologik muammo",
    "details": "rasm haqida batafsil tushuntirish",
    "solution": "muammoni kamaytirish uchun yechim",
    "recommendation": "foydalanuvchiga amaliy tavsiya",
    "eco_score": 0,
    "confidence": 0
}

Qoidalar:

eco_score 0 dan 100 gacha bo'lsin.

confidence 0 dan 100 gacha bo'lsin.

Javob O'zbek tilida bo'lsin.

Agar rasmda ekologik muammo bo'lmasa, buni aniq ayt.

Rasmda ko'rinmaydigan narsalarni aniq fakt sifatida o'ylab topma.
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_data}"
                    }
                ]
            }
        ]
    )

    text = response.output_text

    try:
        data = json.loads(text)

        return data

    except json.JSONDecodeError:
        return {
            "problem": text,
            "details": "",
            "solution": "",
            "recommendation": "",
            "eco_score": 0,
            "confidence": 0
        }