import markdown
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def get_available_chat_models():
    """Groq API'dan sizning kalitingiz uchun AYNAN HOZIR FAOL bo'lgan modellarni dinamik oladi"""
    try:
        models_data = client.models.list().data
        valid_models = []

        # Maxsus, ovozli yoki guard modellarni chetlab o'tamiz
        EXCLUDED_KEYWORDS = ["guard", "whisper", "embed", "vision", "canopy", "orpheus", "safeguard", "audio", "voice"]

        for m in models_data:
            mid = m.id.lower()
            if not any(bad in mid for bad in EXCLUDED_KEYWORDS):
                valid_models.append(m.id)

        # Chat uchun eng kuchli modellarga ustuvorlik beramiz
        valid_models.sort(key=lambda x: (
            0 if "llama-3.3" in x.lower() else
            1 if "llama-3.1" in x.lower() else
            2 if "llama3" in x.lower() else
            3 if "mixtral" in x.lower() else 4
        ))

        return valid_models if valid_models else ["llama3-8b-8192"]
    except Exception as e:
        print(f"⚠️ Modellar ro'yxatini olishda xatolik: {e}")
        return ["llama3-8b-8192"]


def get_chat_response(messages):
    """Mavjud dinamik modellar bo'ylab birma-bir sinab ko'radi"""
    models_to_try = get_available_chat_models()
    print(f"🔍 Topilgan faol modellar ro'yxati: {models_to_try}")

    errors = []
    for model_name in models_to_try:
        try:
            print(f"🚀 Modelga so'rov yuborilmoqda: {model_name}")
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ [{model_name}] ishlamadi: {e}")
            errors.append(f"{model_name}: {e}")
            continue

    last_err = errors[0] if errors else "Hech qaysi model ishlamadi"
    raise Exception(f"Groq API xatosi: {last_err}")


def chat(request):
    if "chat_history" not in request.session:
        request.session["chat_history"] = []

    if request.method == "POST":
        if "clear" in request.POST:
            request.session["chat_history"] = []
            return redirect("/")

        question = request.POST.get("question", "").strip()

        if question:
            history = request.session["chat_history"]
            history.append({"role": "user", "content": question})

            try:
                # Foydalanuvchi tiliga moslashuvchi prompt
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "Siz EcoAI nomli aqlli va do'stona ekologik AI yordamchisiz. "
                            "MANDATORY LANGUAGE RULE: Foydalanuvchi qaysi tilda savol bersa "
                            "(masalan: rus tilida yozsa — FAQAT RUS TILIDA, o'zbek tilida yozsa — O'ZBEK TILIDA, "
                            "ingliz tilida yozsa — INGLIZ TILIDA), javobni AYNAN O'SHA TILDA bering! "
                            "Ekologiya va atrof-muhit nuqtai nazardan atroflicha, aniq va foydali ma'lumot taqdim eting."
                        )
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]

                raw_answer = get_chat_response(messages)

                formatted_answer = mark_safe(
                    markdown.markdown(
                        raw_answer,
                        extensions=['fenced_code', 'tables']
                    )
                )
                history.append({"role": "ai", "content": formatted_answer})

            except Exception as e:
                history.append({
                    "role": "ai",
                    "content": f"⚠️ {str(e)}"
                })

            request.session.modified = True

    return render(request, "ai/chat.html", {
        "chat_history": request.session.get("chat_history", [])
    })