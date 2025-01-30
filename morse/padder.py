from pydub import AudioSegment

# Load the audio files
tones = AudioSegment.from_wav("tones.wav")
base = AudioSegment.from_wav("base.wav")

# Get the duration of each audio file in milliseconds
tones_duration = len(tones)
base_duration = len(base)

# Find the longer duration
duration = max(tones_duration, base_duration)

# Pad the shorter audio file with silence
tones = tones + AudioSegment.silent(duration=duration - tones_duration)
base = base + AudioSegment.silent(duration=duration - base_duration)

# Export padded Soundfiles
tones.export("tones_pad.wav", format="wav")
base.export("base_pad.wav", format="wav")

