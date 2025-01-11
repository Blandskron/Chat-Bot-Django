import requests

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-hf"


def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}", "details": response.text}
    except Exception as err:
        return {"error": f"Other error occurred: {err}"}

output = query({
    "inputs": "Can you please let us know more details about your ",
    "parameters": {
        "max_new_tokens": 100,
        "temperature": 0.7
    }
})

print(output)
