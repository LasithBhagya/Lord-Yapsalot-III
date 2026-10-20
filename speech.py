import sys
import asyncio
import io
from pathlib import Path
import edge_tts
import miniaudio

TEXT = "Bro really spent six and a half fucking hours deep-throating the YouTube algorithm across 9 tabs just to chew through 28 brain-rotting videos, What kind of Olympic-level ADHD doomscrolling speedrun is this, touch some fucking grass you absolute goblin."
OUTPUT_FILE = Path("audio/audio.mp3")
VOICE = "en-US-EmmaNeural"

async def speech(text: str):
    print("Processing the text and preparing the autio track...")

    communicate = edge_tts.Communicate(text, VOICE, pitch="+40Hz", rate="+20%")
    buffer = io.BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buffer.write(chunk["data"])

    audioBytes = buffer.getvalue()
    if not audioBytes:
        raise RuntimeError("Edge TTS returned no audio data.")

    # Save the original MP3.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_bytes(audioBytes)

    # Decode MP3 data into PCM samples.
    decoded = miniaudio.decode(audioBytes, output_format=miniaudio.SampleFormat.SIGNED16)

    # Convert decoded samples to the format expected by miniaudio.
    pcm_bytes = decoded.samples.tobytes()

    # Create a generator that supplies the requested number of frames.
    stream = miniaudio.stream_raw_pcm_memory(pcm_bytes, nchannels=decoded.nchannels, sample_width=decoded.sample_width)

    print(f"Playing audio ({decoded.duration:.2f} seconds)...")

    with miniaudio.PlaybackDevice(output_format=decoded.sample_format, sample_rate=decoded.sample_rate, nchannels=decoded.nchannels) as device:
        next(stream)
        device.start(stream)
        await asyncio.sleep(decoded.duration + 0.2)
        device.stop()

    print(f"Audio saved to: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    asyncio.run(speech(sys.argv[1]))
