import speech_recognition as sr
from pathlib import Path
import numpy as np

class VoiceRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300  # Adjust for sensitivity
        
    def transcribe(self, audio_data) -> str:
        """Convert voice input to text"""
        try:
            if isinstance(audio_data, (np.ndarray, bytes)):
                # Handle raw audio data
                audio = sr.AudioData(audio_data, 16000, 2)  # Sample rate 16kHz, 2 bytes
            elif isinstance(audio_data, str):
                # Handle audio file path
                with sr.AudioFile(audio_data) as source:
                    audio = self.recognizer.record(source)
            else:
                raise ValueError("Unsupported audio input type")
                
            return self.recognizer.recognize_google(audio)
            
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "API unavailable"
        except Exception as e:
            return f"Error processing voice: {str(e)}"