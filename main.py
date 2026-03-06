from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
# from fastrtc_kroko import get_stt_model
from fastrtc import (ReplyOnPause, Stream, KokoroTTSOptions, get_tts_model)
from dotenv import load_dotenv
from fastrtc_whisper_cpp import get_stt_model
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import logging
import os

logger = logging.getLogger("voicebot_logs")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("voicebot.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] - %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] - %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
)
logger.addHandler(stream_handler)


wrapper = DuckDuckGoSearchAPIWrapper(region="in-en", time="d", max_results=5, safesearch="off", source="text")

search = DuckDuckGoSearchResults(api_wrapper=wrapper, output_format="list")

load_dotenv()
checkpointer = InMemorySaver()

# llm = ChatOllama(model='llama3.2:1b')
# llm = ChatOllama(model='hf.co/lm-kit/gemma-3-4b-instruct-gguf:Q4_K_M')

ollama_base_url = os.getenv("OLLAMA_HOST")
llm = ChatOllama(model='qwen3.5:0.8b', base_url=ollama_base_url, think=False)

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="You are an expert Indian financial advisor on a phone call. Use brief, natural sentences to discuss NSE and BSE stocks. Be extremely concise—maximum 1 to 2 short sentences. No lists or disclaimers unless asked. Speak like a quick, helpful human.",
    middleware=[
        SummarizationMiddleware(
            model=llm,
            trigger=("tokens", 4000),
            keep=("messages", 5)
        )
    ],
    checkpointer=checkpointer,
)

options = KokoroTTSOptions(
    voice="af_heart",
    speed=1.2,
    lang="en-us"
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}


stt_model = get_stt_model()
tts_model = get_tts_model()

def echo(audio):
    prompt = stt_model.stt(audio)
    logger.info(f"Here is your prompt: {prompt}")
    response = agent.invoke({"messages": prompt},config)
    prompt = response["messages"][-1].content
    logger.info(f"response: {prompt}")
    for audio_chunk in tts_model.stream_tts_sync(prompt, options=options):
        yield audio_chunk

stream = Stream(ReplyOnPause(echo), modality="audio", mode="send-receive")
stream.ui.launch(share=True)
