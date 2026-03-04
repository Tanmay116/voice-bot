# Voice-to-Voice (V2V) Bot

<!-- ![V2V Hero Image](hero.png) -->

This is a Voice-to-Voice (V2V) web application built with [FastRTC](https://github.com/freddyaboulton/fastrtc), LangChain, and Ollama. It features real-time Speech-to-Text (STT) transcription, integration with a Local LLM (`qwen3.5:0.8b` via Ollama) acting as a concise financial advisor, and Text-to-Speech (TTS) synthesis using Kokoro.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start (with Docker Compose)

The easiest way to run this application is using Docker Compose, which will set up both the application container and an Ollama instance, avoiding configuration headaches.

1. **Start the services:**

   ```bash
   docker-compose up -d --build
   ```

2. **Pull the necessary LLM model into Ollama:**

   Since the Ollama container starts empty, you need to pull the required model (`qwen3.5:0.8b`) the first time you run it.

   ```bash
   docker exec -it ollama ollama run qwen3.5:0.8b
   ```
   *(You can press `Ctrl+D` or type `/bye` to exit the Ollama prompt inside the container once it's downloaded and running).*

3. **Access the Application:**

   Open your web browser and navigate to the Gradio interface at:
   [http://localhost:7860](http://localhost:7860)

## GPU Support (Optional)

If you have an NVIDIA GPU and want to accelerate Ollama execution (recommended for faster LLM response times), you can uncomment the `deploy` section under the `ollama` service in your `docker-compose.yml` file to grant the container access to your GPU.

## How it works

<!-- ![V2V Architecture](architecture.png) -->

The application creates a full voice pipeline:
1. **STT (Speech-to-Text)**: Reads incoming audio to detect spoken user inputs (using FastRTC's Whisper implementation).
2. **LLM**: The transcribed text is sent to an Ollama instance running `qwen3.5:0.8b` behaving as a financial advisor, via `LangChain`.
3. **TTS (Text-to-Speech)**: The advisor's text response is continuously synthesized back into an audio stream for the user using `fastrtc-kokoro-tts`.

## Environment Variables

You can customize the connection to external Ollama instances by setting the connection URL using the `OLLAMA_HOST` environment variable, passed locally or inside Docker Compose.

*Example:* `OLLAMA_HOST=http://your_server_ip:11434`
