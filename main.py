# import os
import ollama
from fastrtc import (ReplyOnPause, Stream, get_stt_model, get_tts_model)
# from groq import Groq
from dotenv import load_dotenv
load_dotenv()

# client = Groq()

stt_model = get_stt_model()
tts_model = get_tts_model()

def echo(audio):
    prompt = stt_model.stt(audio)
    print(f"Here is your prompt: {prompt}")
    # response = client.chat.completions.create(
    #     model="llama-3.1-8b-instant",
    #     messages=[
    #     {
    #         "role": "user",
    #         "content": prompt
    #     }
    #     ],
    #     temperature=1,
    #     max_completion_tokens=512,
    #     top_p=1,
    #     stream=False,
    #     stop=None
    # )
    # prompt = response.choices[0].message.content
    response = ollama.chat(
    model='qwen3:0.6b',
    messages=[
        {'role': 'system', 'content': 'You are a helpful voice assistant. Be extremely concise. Use 1-2 short sentences maximum. Speak naturally like a human in a quick conversation. No bullet points or long explanations'},
        {'role': 'user', 'content': prompt}],
    think=False
)
    prompt = response['message']['content']
    for audio_chunk in tts_model.stream_tts_sync(prompt):
        yield audio_chunk

stream = Stream(ReplyOnPause(echo), modality="audio", mode="send-receive")
stream.ui.launch(share=True)
