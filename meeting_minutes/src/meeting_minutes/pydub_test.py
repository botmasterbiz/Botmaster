from pydub import AudioSegment
from pydub.playback import play

# Generate a simple tone (silence for 1 second)
audio = AudioSegment.silent(duration=1000)  # 1000ms = 1s
print("Audio segment created successfully!")