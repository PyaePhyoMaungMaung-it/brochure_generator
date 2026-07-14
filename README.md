# Brochure Generator

A simple web app that generates a short company brochure from a landing page URL using either Gemini or local Ollama models.

## Features

- Enter a company name and website URL
- Choose between Gemini and Ollama as the generation backend
- Generate a brochure-style response in Markdown
- Run as a local Gradio app

## Requirements

- Python 3.9+
- A Google API key for Gemini (optional if using Ollama)
- Ollama installed and running locally for the Ollama option

## Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root and add your Gemini key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

## Running the App

```bash
python main.py
```

This will launch a local Gradio interface in your browser.

## Ollama Setup

If you want to use Ollama, make sure it is running:

```bash
ollama serve
```

You may also need to pull a model such as:

```bash
ollama pull llama3.2:latest
```

## Project Structure

- `main.py` — main Gradio app and model integration
- `.env` — environment variables

## Notes

- The app uses the OpenAI-compatible API interface for both Gemini and Ollama.
- If Gemini credentials are missing, the app will show a friendly message instead of crashing.
