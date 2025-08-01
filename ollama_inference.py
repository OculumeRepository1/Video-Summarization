def run_ollama(prompt, frames):
    import requests
    import base64
    import cv2

    def encode_image(image):
        _, buffer = cv2.imencode('.jpg', image)
        return base64.b64encode(buffer).decode('utf-8')

    encoded_images = [encode_image(frame) for frame in frames]

    payload = {
        "model": "gemma3:4b",
        "prompt": prompt,
        "images": encoded_images
    }

    response = requests.post("http://localhost:11434/api/generate", json=payload)

    try:
        response_data = response.json()
        print("Ollama Response:", response_data)  # 👈 print entire response
        return response_data["response"]  # this is what caused the KeyError
    except Exception as e:
        print("Failed to decode or parse Ollama response:", e)
        print("Raw response text:", response.text)
        return "❌ Error generating summary from Ollama"
