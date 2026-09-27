import markdown
from django.http import JsonResponse
from django.shortcuts import render, redirect
import os
from django.apps import AppConfig

os.getenv("GROQ_API_KEY")
class AiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ai'

def get_working_chat_model():
    try:
        models = client.models.list().data
        chat_models = [m.id for m in models if not any(b in m.id.lower() for b in ["guard", "whisper", "embed", "vision"])]
        for priority in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama-3.2-3b-instruct"]:
            if priority in chat_models:
                return priority
        return chat_models[0] if chat_models else "llama-3.1-8b-instant"
    except Exception:
        return "llama-3.1-8b-instant"


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
                active_model = get_working_chat_model()
                prompt = (
                    "Siz EcoAI nomli aqlli va do'stona yordamchisiz. "
                    "Har qanday mavzudagi savolga aniq, tushunarli va do'stona javob bering.\n\n"
                    f"Savol: {question}"
                )

                response = client.chat.completions.create(
                    model=active_model,
                    messages=[{"role": "user", "content": prompt}],
                )
                raw_answer = response.choices[0].message.content

                formatted_answer = markdown.markdown(
                    raw_answer, 
                    extensions=['fenced_code', 'tables']
                )
                history.append({"role": "ai", "content": formatted_answer})
                request.session.modified = True

                # Agar AJAX so'rovi bo'lsa, faqat JSON qaytaramiz (sahifa qayta yuklanmaydi)
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        "status": "ok",
                        "user_question": question,
                        "ai_answer": formatted_answer
                    })

            except Exception as e:
                error_msg = f"Groq bilan bog'lanishda xatolik: {str(e)}"
                history.append({"role": "ai", "content": error_msg})
                request.session.modified = True

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({"status": "error", "message": error_msg}, status=500)

    return render(request, "ai/chat.html", {
        "chat_history": request.session.get("chat_history", [])
    })