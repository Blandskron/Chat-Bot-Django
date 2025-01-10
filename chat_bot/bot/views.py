from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings

def llama_bot(request):
    """
    Maneja la interacción con el modelo de Hugging Face.
    """
    user_input = request.GET.get('message') or request.POST.get('message')

    if not user_input:
        return JsonResponse({"error": "El parámetro 'message' es requerido."}, status=400)

    # Configura los encabezados para la API de Hugging Face
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}

    # URL del modelo en Hugging Face
    model_url = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"

    # Enviar la solicitud con parámetros ajustados para obtener respuestas largas y creativas
    payload = {
        "inputs": user_input,
        "parameters": {
            "max_length": 500,  # Respuesta más larga
            "temperature": 0.9,  # Respuesta más creativa
            "top_p": 0.95,  # Aumenta la diversidad en la respuesta
            "top_k": 50,  # Limita el número de opciones para mejorar creatividad
            "repetition_penalty": 1.2,  # Penaliza respuestas repetitivas
            "do_sample": True  # Habilita la generación de muestras para creatividad
        }
    }

    try:
        # Realiza la solicitud a la API de Hugging Face
        response = requests.post(model_url, headers=headers, json=payload)

        # Agregar un log para ver la respuesta completa
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        if response.status_code == 200:
            response_data = response.json()
            generated_text = response_data[0]["generated_text"]
            
            # Elimina cualquier parte del prompt que no se necesite en la respuesta
            clean_text = generated_text.replace(user_input, "").strip()

            return JsonResponse({"response": clean_text})

        elif response.status_code == 422:
            # Respuesta detallada si es un error 422
            return JsonResponse({"error": "Error procesando la solicitud. Verifique los datos enviados.", "details": response.json()}, status=422)

        return JsonResponse({"error": f"Error al obtener respuesta del modelo: {response.status_code}", "details": response.json()}, status=response.status_code)

    except requests.RequestException as e:
        return JsonResponse({"error": f"Error de red: {str(e)}"}, status=500)


def chatbot_view(request):
    return render(request, 'bot/chatbot.html')
