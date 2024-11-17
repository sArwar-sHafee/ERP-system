import os
from dotenv import load_dotenv
import tempfile
import scipy.io.wavfile as wavfile
from openai import OpenAI
from elevenlabs import ElevenLabs, VoiceSettings, play, stream

# Load API keys from .env file
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')

# Initialize clients
openai_client = OpenAI()
elevenlabs_client = ElevenLabs(api_key=elevenlabs_api_key)

# Function to transcribe audio using OpenAI Whisper API
def transcribe(audio):
    if audio is None:
        return "No audio provided.", None
    
    # Audio is received as a tuple (sample_rate, audio_data)
    sample_rate, audio_data = audio
    
    # Save the audio data to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        wavfile.write(temp_file.name, sample_rate, audio_data)
        temp_file_path = temp_file.name

    # Transcribe the audio file using OpenAI Whisper API
    with open(temp_file_path, "rb") as audio_file:
        transcription_response = openai_client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            language="en",
        )
    
    transcription_text = transcription_response.text
    return transcription_text

def tts(response_text):
    # Now, use ElevenLabs to convert the transcription text to speech
    tts_response = elevenlabs_client.text_to_speech.convert(
        voice_id="CwhRBWXzGAHq8TQ4Fs17",
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=response_text,
        voice_settings=VoiceSettings(
            stability=0.1,
            similarity_boost=0.3,
            style=0.2,
        ),
    )
    
    audio_file_path = "output_audio.mp3"
    with open(audio_file_path, "wb") as audio_file:
        for chunk in tts_response:
            audio_file.write(chunk)
    
    return audio_file_path


