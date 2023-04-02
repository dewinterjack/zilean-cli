from dotenv import load_dotenv
load_dotenv()

import os
import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")
# audio_file = open("el3.m4a", "rb")
# transcript = openai.Audio.transcribe("whisper-1", audio_file, response_format="verbose_json")

# print(transcript)

def check_for_audio_cue(data):
    result = openai.Audio.transcribe("whisper-1", data)
    print(result)
    if result.lower() == "hey, zilean":
        print("Zilean is listening")
        return True
    else:
        return False