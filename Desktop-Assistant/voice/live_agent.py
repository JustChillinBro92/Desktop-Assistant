import os
import asyncio
import pyaudio
import numpy as np
import noisereduce as nr

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config.settings import VOICE_MODEL_NAME, VOICE_SYSTEM_PROMPT
from voice.tool_router import run_tool

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

INPUT_SAMPLE_RATE = 16000
OUTPUT_SAMPLE_RATE = 24000
CHUNK_SIZE = 2048

pyaudio_instance = pyaudio.PyAudio()


open_app_tool = {
    "name": "open_app",
    "description": "Open a desktop application installed on the user's computer.",
    "parameters": {
        "type": "object",
        "properties": {
            "app": {
                "type": "string",
                "description": "The name of the desktop app to open."
            }
        },
        "required": ["app"]
    }
}

open_game_tool = {
    "name": "open_game",
    "description": "Open an installed Steam game on the user's computer.",
    "parameters": {
        "type": "object",
        "properties": {
            "game": {
                "type": "string",
                "description": "The name of the game to open."
            }
        },
        "required": ["game"]
    }
}



def record_audio_chunks(seconds=5):
    input_stream = pyaudio_instance.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=INPUT_SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE
    )

    chunks = []

    try:
        for _ in range(int(INPUT_SAMPLE_RATE / CHUNK_SIZE * seconds)):
            chunk = input_stream.read(
                CHUNK_SIZE,
                exception_on_overflow=False
            )
            chunks.append(chunk)

    finally:
        input_stream.stop_stream()
        input_stream.close()

    return chunks



def reduce_noise_chunks(chunks):
    audio_bytes = b"".join(chunks)
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

    reduced = nr.reduce_noise(
        y=audio_np,
        sr=INPUT_SAMPLE_RATE,
        prop_decrease=0.8
    )

    reduced = reduced.astype(np.int16)

    clean_bytes = reduced.tobytes()

    clean_chunks = [
        clean_bytes[i:i + CHUNK_SIZE * 2]
        for i in range(0, len(clean_bytes), CHUNK_SIZE * 2)
    ]

    return clean_chunks



def play_user_audio(audio_chunks):
    output_stream = pyaudio_instance.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=INPUT_SAMPLE_RATE,
        output=True,
        frames_per_buffer=CHUNK_SIZE
    )
        
    try:
        for audio in audio_chunks:
            output_stream.write(audio)
    finally:
        output_stream.stop_stream()
        output_stream.close()
    


async def run_voice_agent(audio_chunks):
    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        system_instruction=VOICE_SYSTEM_PROMPT,
        tools=[
            # 1. Custom Tools
            types.Tool(
                function_declarations=[
                    open_app_tool,
                    open_game_tool
                ]
            )
        ]
    )

    output_stream = pyaudio_instance.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=OUTPUT_SAMPLE_RATE,
        output=True,
        frames_per_buffer=CHUNK_SIZE
    )

    async with client.aio.live.connect(
        model=VOICE_MODEL_NAME,
        config=config
    ) as session:

        for chunk in audio_chunks:
            await session.send_realtime_input(
                audio=types.Blob(
                    data=chunk,
                    mime_type="audio/pcm;rate=16000"
                )
            )
            await asyncio.sleep(0.02)

        await session.send_realtime_input(audio_stream_end=True)

        async for response in session.receive():

            if response.server_content and response.server_content.input_transcription:
                transcript = response.server_content.input_transcription.text
                if transcript:
                    print(f"[YOU]: {transcript}")
                    print(f"[AI]: ", end="", flush=True)
                    
            if response.server_content and response.server_content.output_transcription:
                transcript = response.server_content.output_transcription.text
                if transcript:
                    print(f"{transcript}", end="", flush=True)
                    
            
            if response.server_content and response.server_content.model_turn:
                for part in response.server_content.model_turn.parts:
                    if part.inline_data and part.inline_data.data:
                        output_stream.write(part.inline_data.data)                    

            if response.tool_call:
                for function_call in response.tool_call.function_calls:
                    tool_name = function_call.name
                    args = dict(function_call.args)

                    print(f"[TOOL CALL] {tool_name}({args})\n")

                    result = run_tool(tool_name, args)

                    await session.send_tool_response(
                        function_responses=[
                            types.FunctionResponse(
                                id=function_call.id,
                                name=tool_name,
                                response=result
                            )
                        ]
                    )
                    return

            if response.server_content and response.server_content.turn_complete:
                print("")                
                return



def start_voice_agent():
    try:
        print("")
        print("+---------------------------------------------------------+")
        print("| AI Voice Assistant Started ( Press 'Ctrl + C' to quit ) |")
        print("+---------------------------------------------------------+")

        while True:
            input("\nPress Enter, then speak for 4 seconds...\n"
            "Press 'Ctrl + C' to quit\n")

            print("[VOICE] Recording...")
            chunks = record_audio_chunks(seconds=4)
            chunks = reduce_noise_chunks(chunks)
            # play_user_audio(chunks)

            print("[VOICE] Sending...")
            asyncio.run(run_voice_agent(chunks))

    except KeyboardInterrupt:
        print("\nApplication Closed!\n")

    finally:
        pyaudio_instance.terminate()