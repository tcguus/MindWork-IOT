import cv2
import time
import requests
from deepface import DeepFace

API_URL = "https://localhost:7034/api/v1" 
EMAIL = "iot.device@mindwork.com"         
PASSWORD = "Password123!"

requests.packages.urllib3.disable_warnings()

def login():
    """Faz login na API .NET para pegar o Token JWT"""
    print(f"Tentando logar como {EMAIL}...")
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={"email": EMAIL, "password": PASSWORD},
            verify=False 
        )
        if response.status_code == 200:
            token = response.json().get("token")
            print("Login com sucesso! Token recebido.")
            return token
        else:
            print(f"Erro no login: {response.text}")
            return None
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return None

def send_wellness_event(token, emotion):
    """Envia a emoção detectada para a API"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "userId": None, 
        "eventType": "emotion_detected",
        "source": "office_totem_camera",
        "value": 1.0, 
        "metadataJson": f'{{"detected_emotion": "{emotion}", "confidence": "high"}}'
    }
    
    try:
        resp = requests.post(f"{API_URL}/wellnessevents", json=payload, headers=headers, verify=False)
        if resp.status_code == 201:
            print(f"--> Evento enviado: {emotion}")
        else:
            print(f"Erro ao enviar evento: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Erro de envio: {e}")

def main():
    token = login()
    if not token:
        print("Não foi possível logar. Encerrando.")
        return
    
    cap = cv2.VideoCapture(0)
    
    print("Iniciando monitoramento... Pressione 'q' para sair.")
    last_send_time = 0
    SEND_INTERVAL = 10 

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('MindWork IoT Sensor', frame)

        if time.time() - last_send_time > SEND_INTERVAL:
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                
                if isinstance(result, list):
                    result = result[0]

                dominant_emotion = result['dominant_emotion']
                print(f"Emoção detectada: {dominant_emotion}")
                
                send_wellness_event(token, dominant_emotion)
                
                last_send_time = time.time()
                
            except Exception as e:
                print("Nenhum rosto detectado ou erro na análise.")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()