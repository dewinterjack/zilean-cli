import requests
import json
from io import BytesIO
from pydub import AudioSegment

def generate_speech_file(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/VR6AewLTigWG4xSOukaG"

    payload = json.dumps({
    "text": text,
    "voice_settings": {
        "stability": "0",
        "similarity_boost": "0"
        }
    })

    headers = {
    'xi-api-key': 'b8a82e49685e8a69158bdd2cacdc169e',
    'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload, timeout=500)
    try:
        response.raise_for_status()
        audio_data = BytesIO(response.content)
        audio = AudioSegment.from_file(audio_data, format="mp3")
        audio.export("zil_answer.mp3", format="mp3")
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")